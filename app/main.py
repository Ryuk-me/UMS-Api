from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.utilities.getUptime import getUptime
from fastapi.middleware.cors import CORSMiddleware
from app.routers.v1 import (
    user_router,
    time_table_router,
    announcement_router,
    misc_router,
    hostel_router,
    placement_portal_router,
)
from mangum import Mangum
import time
from app.Config import settings

startTime = time.time()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    docs_url="/docs" if settings.DOCS_ENABLED else None,
    contact={
        "name": "Neeraj Kumar",
        "url": "https://github.com/ryuk-me",
        "email": "neerajkr1210@gmail.com",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_route(req: Request):
    """
    Health Route : Returns App details.

    """
    return JSONResponse(
        {
            "app": settings.APP_NAME,
            "version": "v" + settings.APP_VERSION,
            "ip": req.client.host,
            "uptime": getUptime(startTime),
            "mode": settings.PYTHON_ENV,
        }
    )


app.include_router(user_router.router)
app.include_router(time_table_router.router)
app.include_router(announcement_router.router)
app.include_router(misc_router.router)
app.include_router(hostel_router.router)
app.include_router(placement_portal_router.router)

handler = Mangum(app)
