"""
Optional Feature Nodes - AI-Powered Analysis
TASK-010, 011, 012, 013 implementations
"""
import json
import logging
from ..state import AgentState, StateUpdate
from services.llm import get_llm_service
from services.mcp import get_mcp_service
from services.langsmith import traceable

logger = logging.getLogger(__name__)


@traceable(name="detect_multi_spec", run_type="chain", tags=["agent", "analysis", "multi-spec"])
async def detect_multi_spec_node(state: AgentState) -> StateUpdate:
    """
    Multi-Spec Detection Node (AI-powered)
    TASK-010 Implementation
    """
    logger.info("Multi-spec detection triggered")
    llm_service = get_llm_service()
    
    prompt = f"""
Analise se esta feature deve ser dividida em múltiplas especificações.

FEATURE:
{state.get('feature_summary', '')}

REPOSITÓRIOS SELECIONADOS:
{', '.join(state['selected_repositories'])}

CRITÉRIOS PARA SPLIT:
1. Se 2+ repos têm mudanças significativas (score ≥ 0.70) → Considerar split
2. Mudanças independentes → Favorece split
3. Times diferentes → Favorece split
4. Máximo 4 specs

Responda em JSON:
{{
  "should_split": true/false,
  "affected_repositories": ["repo1", "repo2"],
  "specs": [
    {{
      "repository": "repo1",
      "title": "Feature - Backend",
      "changes_type": "CORE|INTEGRATION|UI_ONLY|CONFIG",
      "effort_days": 3,
      "dependencies": ["repo2"]
    }}
  ],
  "rationale": "Explicação da decisão"
}}
"""
    
    try:
        response = await llm_service.chat_completion(
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0]["message"]["content"])
        
        # Limit to 4 specs max
        if result.get("should_split") and len(result.get("specs", [])) > 4:
            result["specs"] = result["specs"][:4]
            result["rationale"] += " (Limitado a 4 specs para simplicidade)"
        
        logger.info(f"Multi-spec analysis: {result.get('should_split')} - {len(result.get('specs', []))} specs")
        
        return {
            "is_multi_spec": result.get("should_split", False),
            "affected_repositories": result.get("affected_repositories", []),
            "multi_spec_details": result,
            "current_node": "multi_spec"
        }
    except Exception as e:
        logger.error(f"Multi-spec detection error: {e}")
        return {
            "is_multi_spec": False,
            "multi_spec_details": {"error": str(e)},
            "current_node": "multi_spec"
        }


@traceable(name="tech_debt_analysis", run_type="chain", tags=["agent", "analysis", "tech-debt"])
async def tech_debt_node(state: AgentState) -> StateUpdate:
    """
    Tech Debt Analysis Node (AI-powered)
    TASK-011 Implementation
    """
    logger.info("Tech debt analysis triggered")
    llm_service = get_llm_service()
    mcp_service = get_mcp_service()
    
    # Search for potential tech debt in codebase
    search_queries = [
        "complex functions with high cyclomatic complexity",
        "duplicated code patterns",
        "missing error handling",
        "performance bottlenecks",
        "deprecated or legacy code",
        "poor test coverage areas",
        "coupling and dependencies issues"
    ]
    
    code_snippets = []
    for repo in state['selected_repositories']:
        for query in search_queries[:3]:  # Limit queries
            try:
                results = await mcp_service.search_code(repo, query, limit=2)
                code_snippets.extend([r.dict() for r in results])
            except:
                continue
    
    prompt = f"""
Analise dívida técnica neste contexto de código.

FEATURE A IMPLEMENTAR:
{state.get('feature_summary', '')}

CÓDIGO RELEVANTE:
{json.dumps(code_snippets[:5], indent=2)}

Categorias de análise:
1. Code Smells (funções longas, duplicação)
2. Performance (queries N+1, loops ineficientes)
3. Security (inputs sem validação)
4. Testability (código difícil de testar)
5. Coupling (dependências excessivas)
6. Best Practices (antipadrões)
7. Documentation (falta de docs)

Responda em JSON com format exato:
{{
  "issues": [
    {{
      "category": "code_smell|performance|security|testability|coupling|best_practices|documentation",
      "severity": "critical|medium|low",
      "location": "file.py:42",
      "title": "Função muito longa (150 linhas)",
      "description": "Descrição do problema",
      "suggestion": "Como resolver",
      "effort_hours": 2.0,
      "impact_on_feature": "Como afeta a feature atual"
    }}
  ],
  "summary": {{
    "total_issues": 5,
    "total_effort_hours": 8.5,
    "recommendation": "Texto recomendação"
  }}
}}
"""
    
    try:
        response = await llm_service.chat_completion(
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0]["message"]["content"])
        logger.info(f"Tech debt analysis: {result.get('summary', {}).get('total_issues', 0)} issues found")
        
        return {
            "tech_debt_report": result,
            "current_node": "tech_debt"
        }
    except Exception as e:
        logger.error(f"Tech debt analysis error: {e}")
        return {
            "tech_debt_report": {"error": str(e), "issues": []},
            "current_node": "tech_debt"
        }


@traceable(name="security_check", run_type="chain", tags=["agent", "analysis", "security"])
async def security_check_node(state: AgentState) -> StateUpdate:
    """
    Security Checklist Node (LGPD + OWASP)
    TASK-012 Implementation
    """
    logger.info("Security check triggered")
    llm_service = get_llm_service()
    
    prompt = f"""
Analise segurança desta feature.

FEATURE:
{state.get('feature_summary', '')}

DETALHES TÉCNICOS:
{state.get('spec_sections', {}).get('detalhes_tecnicos', 'N/A')}

Categorias de análise:
1. **LGPD** (Lei Geral de Proteção de Dados)
2. **OWASP Top 10**
3. **API Security**
4. **Regras Específicas da Empresa**

Responda em JSON:
{{
  "checks": [
    {{
      "category": "lgpd|owasp|api|company",
      "severity": "critical|high|medium|low",
      "check_id": "LGPD_01",
      "title": "Consentimento para coleta de dados",
      "description": "Feature coleta email do usuário",
      "status": "pass|warning|fail",
      "recommendation": "Adicionar checkbox de consentimento",
      "compliance_reference": "Art. 7º LGPD"
    }}
  ],
  "summary": {{
    "total_checks": 8,
    "critical": 1,
    "warnings": 3,
    "passed": 4,
    "overall_status": "pass|warning|fail"
  }}
}}
"""
    
    try:
        response = await llm_service.chat_completion(
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0]["message"]["content"])
        logger.info(f"Security check: {result.get('summary', {}).get('overall_status', 'unknown')}")
        
        return {
            "security_report": result,
            "current_node": "security"
        }
    except Exception as e:
        logger.error(f"Security check error: {e}")
        return {
            "security_report": {"error": str(e), "checks": []},
            "current_node": "security"
        }


@traceable(name="generate_diagram", run_type="chain", tags=["agent", "diagram", "mermaid"])
async def generate_diagram_node(state: AgentState) -> StateUpdate:
    """
    Mermaid Diagram Generation Node
    TASK-013 Implementation
    """
    logger.info("Diagram generation triggered")
    llm_service = get_llm_service()
    
    prompt = f"""
Gere um diagrama Mermaid para esta feature.

FEATURE:
{state.get('feature_summary', '')}

DETALHES TÉCNICOS:
{state.get('spec_sections', {}).get('detalhes_tecnicos', 'N/A')}

Tipos de diagrama suportados:
1. **flowchart** (fluxos, processos)
2. **sequenceDiagram** (interações entre componentes)
3. **classDiagram** (estrutura de dados)
4. **erDiagram** (entidades e relações)

Escolha o tipo mais adequado e gere código Mermaid válido.

Responda em JSON:
{{
  "diagram_type": "flowchart|sequenceDiagram|classDiagram|erDiagram",
  "mermaid_code": "flowchart TD\\n    A[Start] --> B[End]",
  "title": "Título do diagrama",
  "description": "Explicação do que o diagrama mostra"
}}
"""
    
    try:
        response = await llm_service.chat_completion(
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0]["message"]["content"])
        mermaid_code = result.get("mermaid_code", "graph TD\n    A[Error]")
        
        logger.info(f"Diagram generated: {result.get('diagram_type', 'unknown')}")
        
        return {
            "mermaid_diagram": mermaid_code,
            "current_node": "diagram"
        }
    except Exception as e:
        logger.error(f"Diagram generation error: {e}")
        return {
            "mermaid_diagram": f"graph TD\n    A[Error: {str(e)}]",
            "current_node": "diagram"
        }

