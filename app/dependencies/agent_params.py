from app.schemas.agent import AgentRunRequest
from app.validators.agent import validate_agent_type, resolve_agent_provider
from app.validators.generation import validate_generation_config
from app.validators.timeout import validate_timeout


def agent_params_dependency(req: AgentRunRequest):
    agent_type = validate_agent_type(req.agent_type)

    provider = resolve_agent_provider(req.provider)

    generation_config = validate_generation_config(
        req.generation_config if req.generation_config else None
    )

    timeout = validate_timeout(req.timeout)

    return {
        "agent_type": agent_type,
        "provider": provider,
        "generation_config": generation_config,
        "timeout": timeout,
        "max_steps": req.max_steps,
        "agent_id": req.agent_id,
        "goal": req.goal.strip(),
    }
