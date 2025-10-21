"""
Core Graph Nodes - Main Conversation Loop
Based on LangGraph 0.6.0 async node patterns
"""
import json
import logging
from typing import List, Dict

from ..state import AgentState, StateUpdate
from services.llm import get_llm_service
from services.mcp import get_mcp_service

logger = logging.getLogger(__name__)


async def analyze_feature_node(state: AgentState) -> StateUpdate:
    """
    Analyze user feature request and extract key information.
    
    Based on LangGraph pattern: async node function returning partial state.
    """
    llm_service = get_llm_service()
    
    # Get last user message
    if state["messages"]:
        last_msg = state["messages"][-1]
        # Handle both dict and LangChain message objects
        last_message = last_msg.content if hasattr(last_msg, 'content') else last_msg.get("content", "")
    else:
        last_message = ""
    
    # Análise com LLM
    prompt = f"""
    Analyze this feature request and extract:
    1. Main goal (1-2 sentences)
    2. Affected components (list)
    3. Technical complexity (1-5 scale)
    4. 3 specific questions to ask user
    
    Feature request: {last_message}
    
    Context available:
    - Repositories: {state["selected_repositories"]}
    - User profile: {state["user_profile"]}
    
    Respond in JSON format.
    """
    
    try:
        response = await llm_service.chat_completion(
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            model="google/gemini-2.0-flash-exp:free"
        )
        
        result = json.loads(response.choices[0]["message"]["content"])
        
        logger.info(f"Feature analyzed: {result.get('main_goal', 'N/A')[:50]}...")
        
        return {
            "feature_summary": result.get("main_goal", "Feature analysis pending"),
            "feature_complexity": result.get("complexity", 3),
            "messages": [{
                "role": "assistant",
                "content": f"Entendi! {result.get('main_goal', '')}\n\nPara detalhar melhor:\n" + "\n".join(f"{i+1}. {q}" for i, q in enumerate(result.get("questions", [])))
            }],
            "current_node": "analyze"
        }
    except Exception as e:
        logger.error(f"analyze_feature_node error: {e}")
        return {
            "feature_summary": "Error analyzing feature",
            "current_node": "analyze"
        }


async def search_codebase_node(state: AgentState) -> StateUpdate:
    """
    Search codebase using MCP for relevant context.
    
    Generates search queries based on feature summary and executes them.
    """
    mcp_service = get_mcp_service()
    
    # Generate search queries
    queries = [
        f"implementation of {state['feature_summary']}",
        "related components and dependencies",
        "similar features or patterns",
    ]
    
    all_results = []
    for repo in state["selected_repositories"]:
        for query in queries:
            try:
                results = await mcp_service.search_code(
                    path=repo,
                    query=query,
                    limit=5
                )
                all_results.extend([r.dict() for r in results])
            except Exception as e:
                logger.warning(f"MCP search failed for {repo}: {e}")
                continue
    
    logger.info(f"Found {len(all_results)} code snippets from codebase")
    
    return {
        "codebase_context": all_results[:15],  # Top 15 results
        "current_node": "search"
    }


async def llm_response_node(state: AgentState) -> StateUpdate:
    """
    Generate AI response using context and conversation history.
    
    Uses profile-based prompts from prompts-library.md.
    """
    llm_service = get_llm_service()
    
    # Get appropriate system prompt based on user_profile
    from ..prompts.profiles import get_system_prompt
    system_prompt = get_system_prompt(state["user_profile"])
    
    # Build context
    context_summary = format_codebase_context(state.get("codebase_context", [])[:5])
    
    # Convert messages to dict format for LLM
    messages_for_llm = []
    for msg in state["messages"]:
        if hasattr(msg, 'type'):
            # LangChain message object
            messages_for_llm.append({
                "role": "user" if msg.type == "human" else "assistant",
                "content": msg.content
            })
        elif isinstance(msg, dict):
            messages_for_llm.append(msg)
    
    try:
        # Generate response
        response = await llm_service.chat_completion(
            messages=[
                {"role": "system", "content": system_prompt},
                *messages_for_llm,
                {"role": "system", "content": f"Relevant code context:\n{context_summary}"}
            ],
            model="google/gemini-2.5-pro"
        )
        
        logger.info("LLM response generated")
        
        return {
            "messages": [{
                "role": "assistant",
                "content": response.choices[0]["message"]["content"]
            }],
            "iteration_count": 1,
            "current_node": "llm_response"
        }
    except Exception as e:
        logger.error(f"llm_response_node error: {e}")
        return {
            "messages": [{
                "role": "assistant",
                "content": "Desculpe, ocorreu um erro. Por favor, tente novamente."
            }],
            "current_node": "llm_response"
        }


async def update_spec_node(state: AgentState) -> StateUpdate:
    """
    Update spec sections progressively based on conversation.
    
    Fills company-task-template.md sections as information becomes available.
    """
    llm_service = get_llm_service()
    
    # Extract info for spec sections
    prompt = f"""
    Based on this conversation, extract information to fill these spec sections:
    
    Current sections filled: {list(state["spec_sections"].keys())}
    Recent conversation: {state["messages"][-5:]}
    
    For each section, provide content if enough information is available.
    Return JSON: {{"section_name": "content or null"}}
    
    Sections to fill:
    1. Descrição / Contexto
    2. User Story
    3. Resultado Esperado
    4. Detalhes Técnicos / Escopo
    5. Checklist de Tarefas
    6. Critérios de Aceite
    7. Definição de Done
    8. Observações Adicionais
    9. Referências / Links Úteis
    10. Riscos ou Limitações
    """
    
    try:
        response = await llm_service.chat_completion(
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        updates = json.loads(response.choices[0]["message"]["content"])
        
        # Merge with existing sections
        updated_sections = {**state["spec_sections"], **{k: v for k, v in updates.items() if v}}
        
        logger.info(f"Spec updated: {len(updated_sections)}/10 sections filled")
        
        return {
            "spec_sections": updated_sections,
            "current_node": "update_spec"
        }
    except Exception as e:
        logger.error(f"update_spec_node error: {e}")
        return {
            "current_node": "update_spec"
        }


async def check_completion_node(state: AgentState) -> StateUpdate:
    """
    Calculate spec completion percentage.
    
    Based on filled sections (10 sections total).
    """
    filled_sections = sum(1 for v in state["spec_sections"].values() if v and len(v) > 20)
    total_sections = 10
    
    completion = int((filled_sections / total_sections) * 100)
    
    logger.info(f"Completion check: {completion}% ({filled_sections}/{total_sections} sections)")
    
    return {
        "completion_percentage": completion,
        "current_node": "check_completion"
    }


async def wait_user_input_node(state: AgentState) -> StateUpdate:
    """
    Interrupt point - waits for user input.
    
    This node is marked as interrupt_before in graph compilation.
    """
    logger.info("Waiting for user input...")
    return {
        "current_node": "wait_input"
    }


def format_codebase_context(results: List[Dict]) -> str:
    """Helper to format MCP search results"""
    if not results:
        return "No code context available."
    
    lines = []
    for r in results[:5]:  # Limit to 5 for context window
        lines.append(f"File: {r.get('file', 'unknown')}:{r.get('line', 0)}")
        lines.append(f"```\n{r.get('content', '')}\n```\n")
    return "\n".join(lines)

