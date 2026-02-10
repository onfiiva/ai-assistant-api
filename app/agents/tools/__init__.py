from app.agents.tools.external_api import ExternalAPITool
from app.agents.tools.summary import SummaryTool
from .registry import tool_registry
from .search import SearchTool
from .vector_search_async import VectorSearchTool

tool_registry.register(SearchTool())
tool_registry.register(VectorSearchTool())
tool_registry.register(SummaryTool())
tool_registry.register(ExternalAPITool())
