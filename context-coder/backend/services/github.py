"""
GitHub Projects Integration
Creates cards in GitHub Projects (Backlog, Sprint, Roadmap)
"""
import os
import httpx
import logging
from typing import Dict, Optional, List
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class GitHubCard(BaseModel):
    """GitHub Project card"""
    title: str
    body: str
    project_column: str  # "Backlog", "Sprint", "Roadmap"
    labels: List[str] = []
    repository: Optional[str] = None


class GitHubService:
    """
    GitHub Projects Integration Service
    
    Creates cards in GitHub Projects instead of direct Issues.
    """
    
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.org = os.getenv("GITHUB_ORG")
        self.project_number = int(os.getenv("GITHUB_PROJECT_NUMBER", "1"))
        
        if not self.token:
            logger.warning("GITHUB_TOKEN not set - GitHub integration disabled")
        
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(30.0),
            headers={
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28"
            }
        )
    
    async def create_project_card(
        self,
        card: GitHubCard
    ) -> Dict:
        """
        Create a card in GitHub Projects.
        
        Args:
            card: GitHubCard with title, body, project_column, etc.
        
        Returns:
            Created card details
        
        Note: This is a simplified implementation for MVP.
        Full implementation would use GitHub GraphQL API for Projects V2.
        """
        if not self.token:
            logger.warning("GitHub integration disabled (no token)")
            return {"status": "disabled", "message": "GitHub token not configured"}
        
        try:
            # For MVP: Create as Issue with project label
            # Full implementation would use GraphQL API
            
            repo = card.repository or f"{self.org}/default-repo"
            
            issue_data = {
                "title": card.title,
                "body": card.body,
                "labels": card.labels + [f"project:{card.project_column.lower()}"]
            }
            
            response = await self.client.post(
                f"https://api.github.com/repos/{repo}/issues",
                json=issue_data
            )
            
            response.raise_for_status()
            result = response.json()
            
            logger.info(f"GitHub card created: {result.get('html_url')}")
            
            return {
                "status": "success",
                "issue_number": result.get("number"),
                "url": result.get("html_url"),
                "project_column": card.project_column
            }
        
        except httpx.HTTPStatusError as e:
            logger.error(f"GitHub API error: {e.response.status_code} - {e.response.text}")
            return {"status": "error", "message": f"GitHub API error: {e.response.status_code}"}
        except Exception as e:
            logger.error(f"GitHub integration error: {e}")
            return {"status": "error", "message": str(e)}
    
    async def create_multi_spec_cards(
        self,
        specs: List[Dict],
        base_title: str
    ) -> List[Dict]:
        """
        Create multiple linked cards for multi-spec features.
        
        Args:
            specs: List of spec details (from multi_spec_details)
            base_title: Base feature title
        
        Returns:
            List of created cards
        """
        cards = []
        
        for idx, spec in enumerate(specs[:4]):  # Max 4 specs
            card = GitHubCard(
                title=f"{base_title} - {spec.get('title', f'Part {idx+1}')}",
                body=self._format_spec_body(spec),
                project_column="Backlog",
                labels=["multi-spec", spec.get('repository', 'unknown')],
                repository=spec.get('repository')
            )
            
            result = await self.create_project_card(card)
            cards.append(result)
        
        logger.info(f"Created {len(cards)} multi-spec cards")
        return cards
    
    def _format_spec_body(self, spec: Dict) -> str:
        """Format spec into GitHub Issue body"""
        lines = []
        
        lines.append(f"**Tipo de Mudança**: {spec.get('changes_type', 'N/A')}")
        lines.append(f"**Esforço Estimado**: {spec.get('effort_days', 'N/A')} dias")
        
        if spec.get('dependencies'):
            lines.append(f"**Dependências**: {', '.join(spec['dependencies'])}")
        
        lines.append("\n---\n")
        lines.append("*Gerado por Context2Task*")
        
        return "\n".join(lines)
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()


# Global instance
_github_service = None

def get_github_service() -> GitHubService:
    """Get or create GitHubService singleton"""
    global _github_service
    if _github_service is None:
        _github_service = GitHubService()
    return _github_service


