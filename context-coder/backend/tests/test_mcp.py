"""
Tests for MCP Service (Model Context Protocol)
"""
import pytest
from unittest.mock import Mock, patch, AsyncMock
from services.mcp import MCPService, CodeSearchResult, IndexingStatus


@pytest.fixture
def mock_env(monkeypatch):
    """Mock MCP environment variables"""
    monkeypatch.setenv("OPENAI_API_KEY", "test_openai_key")
    monkeypatch.setenv("ZILLIZ_CLOUD_URI", "https://test.zilliz.cloud")
    monkeypatch.setenv("ZILLIZ_CLOUD_API_KEY", "test_zilliz_key")


def test_mcp_service_init(mock_env):
    """Test MCPService initialization"""
    service = MCPService()
    
    assert service.openai_key == "test_openai_key"
    assert service.zilliz_uri == "https://test.zilliz.cloud"
    assert service.zilliz_key == "test_zilliz_key"


def test_mcp_service_missing_env_vars(monkeypatch):
    """Test MCPService raises error when env vars missing"""
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    
    with pytest.raises(ValueError, match="Missing required environment variables"):
        MCPService()


@pytest.mark.asyncio
async def test_index_codebase(mock_env):
    """Test indexing a codebase"""
    service = MCPService()
    
    mock_result = {
        "status": "success",
        "files_indexed": 150,
        "path": "/test/repo"
    }
    
    with patch.object(service, '_run_npx_command', new_callable=AsyncMock) as mock_run:
        mock_run.return_value = mock_result
        
        result = await service.index_codebase(path="/test/repo")
        
        assert result["status"] == "success"
        assert result["files_indexed"] == 150
        
        # Verify command was called correctly
        mock_run.assert_called_once_with("index-codebase", ["/test/repo"])


@pytest.mark.asyncio
async def test_search_code(mock_env):
    """Test searching codebase"""
    service = MCPService()
    
    mock_result = {
        "results": [
            {
                "file": "src/auth.py",
                "line": 42,
                "content": "def authenticate_user(username, password):",
                "score": 0.95
            },
            {
                "file": "src/models.py",
                "line": 15,
                "content": "class User(Base):",
                "score": 0.87
            }
        ]
    }
    
    with patch.object(service, '_run_npx_command', new_callable=AsyncMock) as mock_run:
        mock_run.return_value = mock_result
        
        results = await service.search_code(
            path="/test/repo",
            query="user authentication",
            limit=5
        )
        
        assert len(results) == 2
        assert isinstance(results[0], CodeSearchResult)
        assert results[0].file == "src/auth.py"
        assert results[0].line == 42
        assert results[0].score == 0.95


@pytest.mark.asyncio
async def test_get_indexing_status(mock_env):
    """Test getting indexing status"""
    service = MCPService()
    
    mock_result = {
        "status": "indexed",
        "file_count": 150,
        "progress": 100
    }
    
    with patch.object(service, '_run_npx_command', new_callable=AsyncMock) as mock_run:
        mock_run.return_value = mock_result
        
        status = await service.get_indexing_status(path="/test/repo")
        
        assert isinstance(status, IndexingStatus)
        assert status.status == "indexed"
        assert status.file_count == 150
        assert status.progress == 100


