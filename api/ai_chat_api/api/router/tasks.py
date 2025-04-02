from enum import Enum

from celery.result import AsyncResult
from fastapi import APIRouter, HTTPException, status, Depends

from ai_chat_api.api.authentication.authenticator import Authenticator
from ai_chat_api.api.common.auth_error import ErrorMessages
from ai_chat_api.celery_app import celery_app


class TaskState(str, Enum):
    PENDING = "PENDING"
    STARTED = "STARTED"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    RETRY = "RETRY"
    REVOKED = "REVOKED"
    PROGRESS = "PROGRESS"


def get_tasks_router(
    authenticator: Authenticator
) -> APIRouter:

    router = APIRouter(prefix="/api/tasks", tags=["tasks"])

    get_current_active_user = authenticator.get_current_user(
        is_active=True, is_verified=True
    )

    @router.get(
        "/{task_id}",
        response_model=dict,
        responses={
            status.HTTP_401_UNAUTHORIZED: {
                "description": ErrorMessages.UNAUTHORIZED.value,
            },
        },
        dependencies=[Depends(get_current_active_user)]
    )
    async def get_threads(task_id: str):
        """
       Check the status of a Celery task and return its state and result.

       Returns:
       - SUCCESS: {status: "success", result: ...}
       - FAILURE: {status: "failed", error: ...}
       - PENDING/STARTED: {status: "pending"/"processing"}
       """

        task = AsyncResult(task_id, app=celery_app)

        if not task:
            raise HTTPException(status_code=400, detail="Task not found")

        if task.state not in TaskState.__members__:
            raise HTTPException(status_code=400, detail="Invalid task state")

        response = {
            "task_id": task_id,
            "status": task.state.lower()
        }

        if task.state == TaskState.SUCCESS:
            response["result"] = task.result
        elif task.state == TaskState.FAILURE:
            response["error"] = str(task.result)
            response["traceback"] = task.traceback
        elif task.state == TaskState.PROGRESS:
            response["progress"] = task.info.get("progress", 0)

        return response

    return router
