"""
MCP Service - Model Context Protocol Integration
Communication with zilliztech/claude-context via npx
"""
import os
import json
import asyncio
import logging
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class CodeSearchResult(BaseModel):
    """Code search result from MCP"""
    file: str
    line: int
    content: str
    score: Optional[float] = None


class IndexingStatus(BaseModel):
    """Codebase indexing status"""
    path: str
    status: str  # "indexed", "indexing", "not_indexed"
    progress: Optional[int] = None  # 0-100 for indexing
    file_count: Optional[int] = None


class MCPService:
    """
    Model Context Protocol Service
    
    Uses zilliztech/claude-context via npx for:
    - index_codebase: Index repositories for search
    - search_code: Semantic search in codebase
    - clear_index: Clear indexed data
    - get_indexing_status: Check indexing progress
    
    Requirements:
    - Node.js 20+ installed (in Docker)
    - npx available
    - OPENAI_API_KEY (for embeddings)
    - ZILLIZ_CLOUD_URI + API_KEY (for vector storage)
    """
    
    def __init__(self):
        # Validate required env vars
        required_vars = ["OPENAI_API_KEY", "ZILLIZ_CLOUD_URI", "ZILLIZ_CLOUD_API_KEY"]
        missing = [v for v in required_vars if not os.getenv(v)]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
        
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.zilliz_uri = os.getenv("ZILLIZ_CLOUD_URI")
        self.zilliz_key = os.getenv("ZILLIZ_CLOUD_API_KEY")
        
        logger.info("MCPService initialized with Zilliz Cloud backend")
    
    async def _run_npx_command(self, command: str, args: List[str]) -> Dict[str, Any]:
        """
        Run npx @zilliztech/claude-context command
        
        Args:
            command: MCP command (index-codebase, search-code, etc.)
            args: Command arguments
        
        Returns:
            Parsed JSON response
        """
        # Build full command
        cmd = ["npx", "@zilliztech/claude-context", command] + args
        
        # Set environment
        env = os.environ.copy()
        env["OPENAI_API_KEY"] = self.openai_key
        env["ZILLIZ_CLOUD_URI"] = self.zilliz_uri
        env["ZILLIZ_CLOUD_API_KEY"] = self.zilliz_key
        
        try:
            logger.debug(f"Running MCP command: {' '.join(cmd[:3])}... (args hidden)")
            
            # Run command
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                error_msg = stderr.decode()
                logger.error(f"MCP command failed: {error_msg}")
                raise RuntimeError(f"MCP command failed: {error_msg}")
            
            # Parse JSON output
            output = stdout.decode()
            result = json.loads(output)
            
            logger.info(f"MCP command succeeded: {command}")
            return result
        
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse MCP response: {e}")
            raise
        except Exception as e:
            logger.error(f"MCP command error: {str(e)}")
            raise
    
    async def index_codebase(
        self,
        path: str,
        force: bool = False,
        custom_extensions: Optional[List[str]] = None,
        ignore_patterns: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Index a codebase for search
        
        Args:
            path: Absolute path to codebase directory
            force: Force re-indexing even if already indexed
            custom_extensions: Additional file extensions (e.g. ['.vue', '.svelte'])
            ignore_patterns: Additional ignore patterns
        
        Returns:
            Indexing result with status
        
        Example:
            ```python
            result = await mcp.index_codebase(
                path="/path/to/repo",
                force=False
            )
            ```
        """
        args = [path]
        
        if force:
            args.append("--force")
        
        if custom_extensions:
            args.extend(["--custom-extensions", ",".join(custom_extensions)])
        
        if ignore_patterns:
            args.extend(["--ignore-patterns", ",".join(ignore_patterns)])
        
        result = await self._run_npx_command("index-codebase", args)
        
        logger.info(f"Indexed codebase: {path}")
        return result
    
    async def search_code(
        self,
        path: str,
        query: str,
        limit: int = 10,
        extension_filter: Optional[List[str]] = None
    ) -> List[CodeSearchResult]:
        """
        Search codebase using natural language query
        
        Args:
            path: Absolute path to indexed codebase
            query: Natural language search query
            limit: Maximum results to return (1-50)
            extension_filter: Filter by file extensions (e.g. ['.ts', '.py'])
        
        Returns:
            List of code search results
        
        Example:
            ```python
            results = await mcp.search_code(
                path="/path/to/repo",
                query="user authentication implementation",
                limit=5
            )
            for r in results:
                print(f"{r.file}:{r.line} - {r.content[:50]}")
            ```
        """
        args = [path, query, str(limit)]
        
        if extension_filter:
            args.extend(["--extension-filter", ",".join(extension_filter)])
        
        result = await self._run_npx_command("search-code", args)
        
        # Parse results
        search_results = [
            CodeSearchResult(
                file=r["file"],
                line=r["line"],
                content=r["content"],
                score=r.get("score")
            )
            for r in result.get("results", [])
        ]
        
        logger.info(f"Found {len(search_results)} results for query: {query}")
        return search_results
    
    async def clear_index(self, path: str) -> Dict[str, Any]:
        """
        Clear search index for a codebase
        
        Args:
            path: Absolute path to codebase
        
        Returns:
            Clearance status
        """
        result = await self._run_npx_command("clear-index", [path])
        
        logger.info(f"Cleared index for: {path}")
        return result
    
    async def get_indexing_status(self, path: str) -> IndexingStatus:
        """
        Get indexing status for a codebase
        
        Args:
            path: Absolute path to codebase
        
        Returns:
            IndexingStatus with status, progress, file_count
        """
        result = await self._run_npx_command("get-indexing-status", [path])
        
        status = IndexingStatus(
            path=path,
            status=result.get("status", "unknown"),
            progress=result.get("progress"),
            file_count=result.get("file_count")
        )
        
        logger.info(f"Indexing status for {path}: {status.status}")
        return status


# Global instance (optional pattern)
_mcp_service = None

def get_mcp_service() -> MCPService:
    """Get or create MCP service singleton"""
    global _mcp_service
    if _mcp_service is None:
        _mcp_service = MCPService()
    return _mcp_service


