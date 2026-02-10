import json
from fastapi import APIRouter, Depends, HTTPException
from app.dependencies.agent_params import agent_params_dependency
from app.dependencies.auth import auth_dependency
from app.models.user import UserContext
from app.schemas.agent import \
    AgentRunRequest, AgentRunResponse, AgentStatusResponse, ToolListResponse
from app.agents.tools.registry import tool_registry
from app.inference.inference_service import InferenceService
from app.dependencies.inference import get_inference_service

router = APIRouter(
    prefix="/agents",
    tags=["Agents"]
)


@router.post("/run", response_model=AgentRunResponse)
async def run_agent(
    req: AgentRunRequest,
    params=Depends(agent_params_dependency),
    user: UserContext = Depends(auth_dependency),
    inference_service: InferenceService = Depends(get_inference_service),
):
    if not params["goal"]:
        raise HTTPException(status_code=400, detail="Goal cannot be empty")

    job_payload = {
        "agent_type": params["agent_type"],
        "agent_id": params["agent_id"],
        "goal": params["goal"],
        "max_steps": params["max_steps"],
        "provider": params["provider"],
        "generation_config": params["generation_config"],
        "timeout": params["timeout"],
    }

    job_id = await inference_service.create_job(
        prompt=json.dumps(job_payload),
        model=params["provider"],
        temperature=params["generation_config"].get("temperature", 0.7),
        user_id=user.id,
    )

    return AgentRunResponse(job_id=str(job_id))


@router.get("/{job_id}", response_model=AgentStatusResponse)
async def get_agent_status(
    job_id: str,
    inference_service: InferenceService = Depends(get_inference_service),
    user: UserContext = Depends(auth_dependency),
):
    """
    Get current agent status and steps history
    """
    status = await inference_service.get_job_status(job_id)
    if not status:
        raise HTTPException(status_code=404, detail="Job not found")
    return AgentStatusResponse(**status)


@router.get("/tools", response_model=ToolListResponse)
async def get_tools(
    user: UserContext = Depends(auth_dependency),
):
    """
    Return list of available tools for the agent.
    """
    return ToolListResponse(tools=tool_registry.list_tools())
