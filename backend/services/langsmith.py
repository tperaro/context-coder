"""
Módulo de integração do LangSmith para rastreamento e observabilidade.

Este módulo fornece integração completa com o LangSmith para rastreamento
de execuções do LangGraph, debugging e avaliação de performance do Context-Coder.

Features:
- Configuração automática via variáveis de ambiente
- Rastreamento de execuções do LangGraph (agent nodes)
- Context manager para rastreamento customizado
- Decorador @traceable para funções personalizadas
- Ocultação de dados sensíveis em traces
- Métricas e tags customizadas

Documentação: https://docs.smith.langchain.com/
"""

from __future__ import annotations

import logging
import os
from contextlib import contextmanager
from functools import wraps
from typing import Any, Callable, Dict, Generator, List, Literal, Optional, TypeVar

from langsmith import Client
from langsmith import traceable as langsmith_traceable

logger = logging.getLogger(__name__)

# Type variable para decoradores
F = TypeVar("F", bound=Callable[..., Any])

# Tipos para run_type
RunType = Literal["tool", "chain", "llm", "retriever", "embedding", "prompt", "parser"]


class LangSmithConfig:
    """Configuração centralizada do LangSmith."""

    def __init__(self):
        """Inicializa a configuração do LangSmith a partir das variáveis de ambiente."""
        # Suporta ambas as variantes: LANGSMITH_* (novo) e LANGCHAIN_* (legacy/LangChain)
        # para máxima compatibilidade
        self.tracing_enabled = (
            os.getenv("LANGSMITH_TRACING", "false").lower() == "true" or
            os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
        )
        # API key - tenta ambas as variantes
        self.api_key = os.getenv("LANGSMITH_API_KEY") or os.getenv("LANGCHAIN_API_KEY")
        # Endpoint - tenta ambas as variantes
        self.endpoint = (
            os.getenv("LANGSMITH_ENDPOINT") or 
            os.getenv("LANGCHAIN_ENDPOINT") or 
            "https://api.smith.langchain.com"
        )
        # Project name - tenta ambas as variantes
        self.project_name = (
            os.getenv("LANGSMITH_PROJECT") or 
            os.getenv("LANGCHAIN_PROJECT") or 
            "context-coder"
        )
        self.workspace_id = os.getenv("LANGSMITH_WORKSPACE_ID")

        # Validação básica
        if self.tracing_enabled and not self.api_key:
            logger.warning(
                "LangSmith tracing está habilitado mas LANGSMITH_API_KEY/LANGCHAIN_API_KEY "
                "não foi configurada. O rastreamento será desabilitado."
            )
            self.tracing_enabled = False

    def is_configured(self) -> bool:
        """Verifica se o LangSmith está configurado corretamente."""
        return self.tracing_enabled and bool(self.api_key)

    def get_client(
        self,
        hide_inputs: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None,
        hide_outputs: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None,
    ) -> Client:
        """
        Retorna um cliente LangSmith configurado.

        Args:
            hide_inputs: Função para ocultar dados sensíveis dos inputs
            hide_outputs: Função para ocultar dados sensíveis dos outputs

        Returns:
            Cliente LangSmith configurado
        """
        return Client(
            api_key=self.api_key,
            api_url=self.endpoint,
            hide_inputs=hide_inputs,
            hide_outputs=hide_outputs,
        )


# Instância global de configuração
config = LangSmithConfig()


def is_langsmith_enabled() -> bool:
    """
    Verifica se o LangSmith está habilitado e configurado.

    Returns:
        True se o LangSmith estiver habilitado e configurado
    """
    return config.is_configured()


def get_langsmith_client(
    hide_inputs: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None,
    hide_outputs: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None,
) -> Optional[Client]:
    """
    Retorna um cliente LangSmith se estiver configurado, caso contrário None.

    Args:
        hide_inputs: Função para ocultar dados sensíveis dos inputs
        hide_outputs: Função para ocultar dados sensíveis dos outputs

    Returns:
        Cliente LangSmith ou None se não estiver configurado
    """
    if not config.is_configured():
        return None

    return config.get_client(hide_inputs=hide_inputs, hide_outputs=hide_outputs)


@contextmanager
def trace_context(
    client: Optional[Client] = None,
    project_name: Optional[str] = None,
    tags: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> Generator[None, None, None]:
    """
    Context manager para rastreamento com LangSmith.
    
    Nota: Com a versão atual do LangSmith, o rastreamento é automático
    quando as variáveis de ambiente estão configuradas. Este context manager
    permite sobrescrever temporariamente o projeto e adicionar tags/metadata.

    Uso:
        with trace_context(tags=["production", "feature-analysis"]):
            result = my_function()

    Args:
        client: Cliente LangSmith customizado (opcional, não utilizado na versão atual)
        project_name: Nome do projeto para este trace (opcional)
        tags: Tags para adicionar ao trace (aplicadas via metadata de configuração)
        metadata: Metadados adicionais para o trace

    Yields:
        None
    """
    if not config.is_configured():
        logger.debug("LangSmith não está configurado, pulando rastreamento")
        yield
        return

    # Salvar valores originais (ambas as variantes para compatibilidade)
    original_project_new = os.environ.get("LANGSMITH_PROJECT")
    original_project_legacy = os.environ.get("LANGCHAIN_PROJECT")
    
    # Aplicar configurações temporárias
    if project_name:
        os.environ["LANGSMITH_PROJECT"] = project_name
        os.environ["LANGCHAIN_PROJECT"] = project_name  # Para compatibilidade com LangChain

    try:
        # O rastreamento é automático com LangSmith SDK
        # Tags e metadata são aplicadas via create_run_config nas chamadas individuais
        yield
    finally:
        # Restaurar valores originais
        if project_name:
            if original_project_new:
                os.environ["LANGSMITH_PROJECT"] = original_project_new
            else:
                os.environ.pop("LANGSMITH_PROJECT", None)
            
            if original_project_legacy:
                os.environ["LANGCHAIN_PROJECT"] = original_project_legacy
            else:
                os.environ.pop("LANGCHAIN_PROJECT", None)


def traceable(
    name: Optional[str] = None,
    run_type: RunType = "chain",
    tags: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> Callable[[F], F]:
    """
    Decorador para rastrear funções com LangSmith.

    Uso:
        @traceable(name="analyze_feature", run_type="chain", tags=["agent", "analysis"])
        def analyze_feature(feature_data: dict) -> dict:
            return {"analysis": "..."}

    Args:
        name: Nome customizado para o trace (opcional, usa nome da função)
        run_type: Tipo de execução ("chain", "llm", "tool", "retriever", etc)
        tags: Tags para organizar traces
        metadata: Metadados adicionais

    Returns:
        Função decorada com rastreamento
    """

    def decorator(func: F) -> F:
        if not config.is_configured():
            # Se não estiver configurado, retorna função original
            return func

        # Aplicar decorador do langsmith com os parâmetros corretos
        # O langsmith_traceable aceita os parâmetros diretamente
        traced_func = langsmith_traceable(
            name=name,
            run_type=run_type,
            tags=tags,
            metadata=metadata
        )(func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            return traced_func(*args, **kwargs)

        # If the original function was async, return an async wrapper that awaits the traced func
        try:
            import inspect

            if inspect.iscoroutinefunction(func):
                async def async_wrapper(*args, **kwargs):
                    return await traced_func(*args, **kwargs)

                return async_wrapper  # type: ignore
        except Exception:
            # Fallback to sync wrapper
            pass

        return wrapper  # type: ignore

    return decorator


def hide_sensitive_data(
    data: Dict[str, Any],
    sensitive_keys: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Oculta dados sensíveis de um dicionário para traces.

    Args:
        data: Dicionário com dados
        sensitive_keys: Lista de chaves a serem ocultadas (padrão: senhas, tokens, etc)

    Returns:
        Dicionário com dados sensíveis ocultados
    """
    if sensitive_keys is None:
        sensitive_keys = [
            "password",
            "senha",
            "token",
            "api_key",
            "secret",
            "authorization",
            "credentials",
            "cpf",
            "rg",
            "phone",
            "telefone",
            "email",
            "github_token",
            "openrouter_key",
            "google_api_key",
        ]

    result = data.copy()

    for key in result.keys():
        key_lower = key.lower()
        if any(sensitive in key_lower for sensitive in sensitive_keys):
            result[key] = "***HIDDEN***"

    return result


def create_run_config(
    run_name: Optional[str] = None,
    tags: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Cria um dicionário de configuração para passar ao graph.stream() ou graph.invoke().

    Uso:
        config = create_run_config(
            run_name="feature_spec_session_123",
            tags=["production", "feature_analysis"],
            metadata={"user_profile": "technical", "repo": "myrepo"}
        )
        result = graph.invoke(inputs, config)

    Args:
        run_name: Nome customizado para esta execução
        tags: Tags para organizar execuções
        metadata: Metadados adicionais

    Returns:
        Dicionário de configuração para LangGraph
    """
    config: Dict[str, Any] = {}

    if run_name:
        config["run_name"] = run_name

    if tags:
        config["tags"] = tags

    if metadata:
        config["metadata"] = metadata

    return config


def log_langsmith_status() -> None:
    """Loga o status da configuração do LangSmith."""
    if config.is_configured():
        logger.info(
            f"✓ LangSmith configurado - Projeto: {config.project_name}, "
            f"Endpoint: {config.endpoint}"
        )
    else:
        logger.info("✗ LangSmith não está configurado ou desabilitado")


# Exportar configurações e funções principais
__all__ = [
    "LangSmithConfig",
    "config",
    "is_langsmith_enabled",
    "get_langsmith_client",
    "trace_context",
    "traceable",
    "hide_sensitive_data",
    "create_run_config",
    "log_langsmith_status",
]
