"""
Markdown Export Service
Validates and formats specs according to company-task-template.md
"""
import logging
from typing import Dict, List, Optional
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class ExportValidation(BaseModel):
    """Validation result for spec export"""
    is_valid: bool
    filled_sections: int
    total_sections: int
    missing_sections: List[str]
    warnings: List[str]


class MarkdownExporter:
    """
    Export specifications to Markdown format.
    
    Based on company-task-template.md with 10 required sections.
    """
    
    REQUIRED_SECTIONS = [
        "descricao_contexto",
        "user_story",
        "resultado_esperado",
        "detalhes_tecnicos",
        "checklist_tarefas",
        "criterios_aceite",
        "definicao_done",
        "observacoes",
        "referencias",
        "riscos_limitacoes"
    ]
    
    SECTION_TITLES = {
        "descricao_contexto": "📌 Descrição / Contexto",
        "user_story": "👤 User Story",
        "resultado_esperado": "📋 Resultado Esperado",
        "detalhes_tecnicos": "⚙️ Detalhes Técnicos / Escopo",
        "checklist_tarefas": "📌 Checklist de Tarefas",
        "criterios_aceite": "✅ Critérios de Aceite",
        "definicao_done": "📦 Definição de Done",
        "observacoes": "🔍 Observações Adicionais",
        "referencias": "🔗 Referências / Links Úteis",
        "riscos_limitacoes": "⚠️ Riscos ou Limitações"
    }
    
    def validate(self, spec_sections: Dict[str, str]) -> ExportValidation:
        """
        Validate spec completeness.
        
        Args:
            spec_sections: Dict with section keys and content
        
        Returns:
            ExportValidation with validation results
        """
        filled = []
        missing = []
        warnings = []
        
        for section in self.REQUIRED_SECTIONS:
            content = spec_sections.get(section, "")
            if content and len(content.strip()) > 20:
                filled.append(section)
            else:
                missing.append(self.SECTION_TITLES.get(section, section))
        
        # Warnings
        if len(filled) < 8:
            warnings.append(f"Apenas {len(filled)}/10 seções preenchidas. Recomendamos completar pelo menos 8 seções.")
        
        return ExportValidation(
            is_valid=len(filled) >= 8,  # At least 80% complete
            filled_sections=len(filled),
            total_sections=len(self.REQUIRED_SECTIONS),
            missing_sections=missing,
            warnings=warnings
        )
    
    def export_to_markdown(
        self,
        spec_sections: Dict[str, str],
        feature_title: str = "Nova Feature",
        metadata: Optional[Dict] = None
    ) -> str:
        """
        Export spec to Markdown format.
        
        Args:
            spec_sections: Dict with section content
            feature_title: Title for the spec
            metadata: Optional metadata (session_id, user_profile, etc.)
        
        Returns:
            Formatted Markdown string
        """
        lines = []
        
        # Header
        lines.append(f"# {feature_title}\n")
        
        if metadata:
            lines.append("---")
            lines.append(f"**Criado por**: Context2Task AI")
            lines.append(f"**Perfil**: {metadata.get('user_profile', 'N/A')}")
            lines.append(f"**Session ID**: {metadata.get('session_id', 'N/A')}")
            lines.append(f"**Completude**: {metadata.get('completion_percentage', 0)}%")
            lines.append("---\n")
        
        # Sections
        for section_key in self.REQUIRED_SECTIONS:
            title = self.SECTION_TITLES.get(section_key, section_key)
            content = spec_sections.get(section_key, "")
            
            lines.append(f"## {title}\n")
            
            if content and content.strip():
                lines.append(f"{content.strip()}\n")
            else:
                lines.append("*[Seção não preenchida]*\n")
            
            lines.append("")  # Blank line
        
        # Footer
        lines.append("---")
        lines.append("*Gerado por Context2Task - AI-Powered Feature Specification Platform*")
        
        return "\n".join(lines)
    
    def export_json(self, spec_sections: Dict[str, str], metadata: Optional[Dict] = None) -> Dict:
        """
        Export spec as JSON (for API responses).
        
        Args:
            spec_sections: Dict with section content
            metadata: Optional metadata
        
        Returns:
            JSON-serializable dict
        """
        validation = self.validate(spec_sections)
        
        return {
            "spec_sections": spec_sections,
            "validation": validation.dict(),
            "metadata": metadata or {},
            "format_version": "1.0"
        }


# Global instance
_exporter = None

def get_exporter() -> MarkdownExporter:
    """Get or create MarkdownExporter singleton"""
    global _exporter
    if _exporter is None:
        _exporter = MarkdownExporter()
    return _exporter


