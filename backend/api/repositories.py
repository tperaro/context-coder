"""
Repository Discovery API Endpoints
Discover and manage repositories for MCP integration
"""
import os
import asyncio
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from services.mcp import get_mcp_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/repositories", tags=["repositories"])


# ===== REQUEST/RESPONSE MODELS =====

class RepositoryInfo(BaseModel):
    """Repository information"""
    path: str
    name: str
    is_indexed: bool
    indexing_status: Optional[str] = None
    file_count: Optional[int] = None
    last_modified: Optional[str] = None


class DiscoverRepositoriesResponse(BaseModel):
    """Response for repository discovery"""
    repositories: List[RepositoryInfo]
    total_found: int
    indexed_count: int


class IndexRepositoryRequest(BaseModel):
    """Request to index a repository"""
    path: str
    force: bool = False


class IndexRepositoryResponse(BaseModel):
    """Response for repository indexing"""
    path: str
    status: str
    message: str
    file_count: Optional[int] = None


# ===== HELPER FUNCTIONS =====

def is_git_repository(path: Path) -> bool:
    """Check if directory is a git repository"""
    return (path / '.git').exists()


def get_common_repo_paths() -> List[Path]:
    """Get common repository directory paths"""
    home = Path.home()
    common_paths = [
        home / 'git',
        home / 'projects',
        home / 'workspace',
        home / 'dev',
        home / 'repos',
        home / 'code',
        home / 'src',
        Path('/home') / os.getenv('USER', '') / 'git',
        Path('/home') / os.getenv('USER', '') / 'projects',
    ]
    
    # Filter only existing paths
    return [p for p in common_paths if p.exists()]


async def scan_directory_for_repos(base_path: Path) -> List[Path]:
    """Scan directory for git repositories"""
    repositories = []
    
    try:
        # Look for direct git repos in the base path
        if is_git_repository(base_path):
            repositories.append(base_path)
        
        # Look for subdirectories that are git repos
        for item in base_path.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                if is_git_repository(item):
                    repositories.append(item)
                
                # Recursively scan one level deeper for common patterns
                if item.name in ['projects', 'workspace', 'dev', 'repos', 'code']:
                    for subitem in item.iterdir():
                        if subitem.is_dir() and not subitem.name.startswith('.') and is_git_repository(subitem):
                            repositories.append(subitem)
    
    except PermissionError:
        logger.warning(f"Permission denied accessing {base_path}")
    except Exception as e:
        logger.error(f"Error scanning {base_path}: {e}")
    
    return repositories


async def check_repository_indexing_status(mcp_service, repo_path: str) -> Dict[str, Any]:
    """Check if repository is indexed in MCP"""
    try:
        status = await mcp_service.get_indexing_status(repo_path)
        return {
            'is_indexed': status.status == 'indexed',
            'status': status.status,
            'file_count': status.file_count,
            'progress': status.progress
        }
    except Exception as e:
        logger.warning(f"Could not check indexing status for {repo_path}: {e}")
        return {
            'is_indexed': False,
            'status': 'unknown',
            'file_count': None,
            'progress': None
        }


# ===== ENDPOINTS =====

@router.get("/discover", response_model=DiscoverRepositoriesResponse)
async def discover_repositories():
    """
    Discover repositories in common directories and check MCP indexing status.
    
    Scans common development directories for git repositories and checks
    which ones are already indexed in the MCP system.
    """
    try:
        # Get common repository paths
        common_paths = get_common_repo_paths()
        
        if not common_paths:
            return DiscoverRepositoriesResponse(
                repositories=[],
                total_found=0,
                indexed_count=0
            )
        
        # Scan all common paths for repositories
        all_repos = []
        for base_path in common_paths:
            repos = await scan_directory_for_repos(base_path)
            all_repos.extend(repos)
        
        # Remove duplicates and sort
        unique_repos = list(set(all_repos))
        unique_repos.sort(key=lambda p: str(p))
        
        # Get MCP service
        mcp_service = get_mcp_service()
        
        # Check indexing status for each repository
        repositories = []
        indexed_count = 0
        
        for repo_path in unique_repos:
            repo_str = str(repo_path)
            indexing_info = await check_repository_indexing_status(mcp_service, repo_str)
            
            repo_info = RepositoryInfo(
                path=repo_str,
                name=repo_path.name,
                is_indexed=indexing_info['is_indexed'],
                indexing_status=indexing_info['status'],
                file_count=indexing_info['file_count']
            )
            
            repositories.append(repo_info)
            if indexing_info['is_indexed']:
                indexed_count += 1
        
        logger.info(f"Discovered {len(repositories)} repositories, {indexed_count} indexed")
        
        return DiscoverRepositoriesResponse(
            repositories=repositories,
            total_found=len(repositories),
            indexed_count=indexed_count
        )
    
    except Exception as e:
        logger.error(f"Error discovering repositories: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to discover repositories: {str(e)}"
        )


@router.get("/available", response_model=List[RepositoryInfo])
async def get_available_repositories():
    """
    Get list of repositories that are already indexed in MCP.
    
    This is a simplified version that returns repositories from discovery
    that are already indexed. In a full implementation, you might want
    to query MCP directly for indexed repositories.
    """
    try:
        # For now, use discovery and filter indexed ones
        discover_response = await discover_repositories()
        indexed_repos = [repo for repo in discover_response.repositories if repo.is_indexed]
        
        logger.info(f"Found {len(indexed_repos)} available indexed repositories")
        return indexed_repos
    
    except Exception as e:
        logger.error(f"Error getting available repositories: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get available repositories: {str(e)}"
        )


@router.post("/index", response_model=IndexRepositoryResponse)
async def index_repository(request: IndexRepositoryRequest):
    """
    Index a repository using MCP.
    
    This will index the specified repository path using the MCP service,
    making it available for semantic search.
    """
    try:
        # Validate path exists
        repo_path = Path(request.path)
        if not repo_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Repository path does not exist: {request.path}"
            )
        
        if not is_git_repository(repo_path):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Path is not a git repository: {request.path}"
            )
        
        # Get MCP service and index repository
        mcp_service = get_mcp_service()
        
        logger.info(f"Starting indexing for repository: {request.path}")
        
        # Index the repository
        result = await mcp_service.index_codebase(
            path=request.path,
            force=request.force
        )
        
        # Get file count from result
        file_count = result.get('file_count', 0)
        
        logger.info(f"Successfully indexed repository: {request.path} ({file_count} files)")
        
        return IndexRepositoryResponse(
            path=request.path,
            status="success",
            message=f"Repository indexed successfully with {file_count} files",
            file_count=file_count
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error indexing repository {request.path}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to index repository: {str(e)}"
        )


@router.get("/status/{path:path}")
async def get_repository_status(path: str):
    """
    Get indexing status for a specific repository.
    
    Returns detailed information about the repository's indexing status
    in the MCP system.
    """
    try:
        mcp_service = get_mcp_service()
        status = await mcp_service.get_indexing_status(path)
        
        return {
            "path": path,
            "status": status.status,
            "progress": status.progress,
            "file_count": status.file_count,
            "is_indexed": status.status == "indexed"
        }
    
    except Exception as e:
        logger.error(f"Error getting status for {path}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get repository status: {str(e)}"
        )
