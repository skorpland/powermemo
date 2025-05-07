from ..controllers import full as controllers


from ..models.blob import BlobType
from ..models import response as res
from fastapi import Request
from fastapi import Path


async def flush_buffer(
    request: Request,
    user_id: str = Path(..., description="The ID of the user"),
    buffer_type: BlobType = Path(..., description="The type of buffer to flush"),
) -> res.ChatModalAPIResponse:
    """Get the real-time user profiles for long term memory"""
    project_id = request.state.powermemo_project_id
    p = await controllers.buffer.wait_insert_done_then_flush(
        user_id, project_id, buffer_type
    )
    return p.to_response(res.ChatModalAPIResponse)
