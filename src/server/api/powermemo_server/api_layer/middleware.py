import os
import time
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse

from ..env import ProjectStatus
from ..models.database import DEFAULT_PROJECT_ID
from ..models.utils import Promise
from ..telemetry import (
    telemetry_manager,
    CounterMetricName,
    HistogramMetricName,
)
from ..models.response import BaseResponse, CODE
from ..auth.token import (
    parse_project_id,
    check_project_secret,
    get_project_status,
)


PATH_MAPPINGS = [
    "/api/v1/users/blobs",
    "/api/v1/users/profile",
    "/api/v1/users/buffer",
    "/api/v1/users/event",
    "/api/v1/users/context",
    "/api/v1/users",
    "/api/v1/blobs/insert",
    "/api/v1/blobs",
]


class AuthMiddleware(BaseHTTPMiddleware):
    def normalize_path(self, path: str) -> str:
        """Remove dynamic path parameters to get normalized path for metrics"""
        if not path.startswith("/api"):
            return path

        for prefix in PATH_MAPPINGS:
            if path.startswith(prefix):
                return prefix

        return path

    async def dispatch(self, request, call_next):
        if not request.url.path.startswith("/api"):
            return await call_next(request)

        if request.url.path.startswith("/api/v1/healthcheck"):
            telemetry_manager.increment_counter_metric(
                CounterMetricName.HEALTHCHECK,
                1,
            )
            return await call_next(request)

        auth_token = request.headers.get("Authorization")
        if not auth_token or not auth_token.startswith("Bearer "):
            return JSONResponse(
                status_code=CODE.UNAUTHORIZED.value,
                content=BaseResponse(
                    errno=CODE.UNAUTHORIZED.value,
                    errmsg=f"Unauthorized access to {request.url.path}. You have to provide a valid Bearer token.",
                ).model_dump(),
            )
        auth_token = (auth_token.split(" ")[1]).strip()
        is_root = self.is_valid_root(auth_token)
        request.state.is_powermemo_root = is_root
        request.state.powermemo_project_id = DEFAULT_PROJECT_ID
        if not is_root:
            p = await self.parse_project_token(auth_token)
            if not p.ok():
                return JSONResponse(
                    status_code=CODE.UNAUTHORIZED.value,
                    content=BaseResponse(
                        errno=CODE.UNAUTHORIZED.value,
                        errmsg=f"Unauthorized access to {request.url.path}. {p.msg()}",
                    ).model_dump(),
                )
            request.state.powermemo_project_id = p.data()
        # await capture_int_key(TelemetryKeyName.has_request)

        normalized_path = self.normalize_path(request.url.path)

        telemetry_manager.increment_counter_metric(
            CounterMetricName.REQUEST,
            1,
            {
                "project_id": request.state.powermemo_project_id,
                "path": normalized_path,
                "method": request.method,
            },
        )

        start_time = time.time()
        response = await call_next(request)

        telemetry_manager.record_histogram_metric(
            HistogramMetricName.REQUEST_LATENCY_MS,
            (time.time() - start_time) * 1000,
            {
                "project_id": request.state.powermemo_project_id,
                "path": normalized_path,
                "method": request.method,
            },
        )
        return response

    def is_valid_root(self, token: str) -> bool:
        access_token = os.getenv("ACCESS_TOKEN")
        if access_token is None:
            return True
        return token == access_token.strip()

    async def parse_project_token(self, token: str) -> Promise[str]:
        p = parse_project_id(token)
        if not p.ok():
            return Promise.reject(CODE.UNAUTHORIZED, "Invalid project id format")
        project_id = p.data()
        p = await check_project_secret(project_id, token)
        if not p.ok():
            return p
        if not p.data():
            return Promise.reject(CODE.UNAUTHORIZED, "Wrong secret key")
        p = await get_project_status(project_id)
        if not p.ok():
            return p
        if p.data() == ProjectStatus.suspended:
            return Promise.reject(CODE.FORBIDDEN, "Your project is suspended!")
        return Promise.resolve(project_id)
