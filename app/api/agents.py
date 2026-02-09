import json
from fastapi import APIRouter, Depends, HTTPException
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
    request: AgentRunRequest,
    inference_service: InferenceService = Depends(get_inference_service)
):
    """
    Launch ReAct agent with a given target
    Returns the job_id for asynchronous result retrieval.
    """
    # Prepare payload for worker
    payload = {
        "agent_type": "react",
        "goal": request.goal,
        "max_steps": request.max_steps
    }

    # Create async job via inference service
    job_id = await inference_service.create_job(
        prompt=json.dumps(payload),
        model="default",
        temperature=0.7
    )

    return AgentRunResponse(job_id=str(job_id))


@router.get("/{job_id}", response_model=AgentStatusResponse)
async def get_agent_status(
    job_id: str,
    inference_service: InferenceService = Depends(get_inference_service)
):
    """
    Get current agent status and steps history
    """
    status = await inference_service.get_job_status(job_id)
    if not status:
        raise HTTPException(status_code=404, detail="Job not found")
    return AgentStatusResponse(**status)


@router.get("/tools", response_model=ToolListResponse)
async def get_tools():
    """
    Return list of available tools for the agent.
    """
    return ToolListResponse(tools=tool_registry.list_tools())
