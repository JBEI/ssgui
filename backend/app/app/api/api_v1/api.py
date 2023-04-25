from fastapi import APIRouter

from app.api.api_v1.endpoints import (
    login,
    users,
    utils,
    standalone,
    templates,
    runs,
    samples,
    db,
    snapshots,
)

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(runs.router, tags=["runs"])
api_router.include_router(templates.router, tags=["templates"])
api_router.include_router(samples.router, tags=["samples"])
api_router.include_router(standalone.router, tags=["standalone"])
api_router.include_router(db.router, tags=["db"])
api_router.include_router(snapshots.router, tags=["snapshots"])
