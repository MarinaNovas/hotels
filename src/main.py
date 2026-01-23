import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI

sys.path.append(str(Path(__file__).parent.parent))

from src.api.auth import router as router_auth
from src.api.hotels import router as router_hotels


app = FastAPI()
app.include_router(router_hotels)
app.include_router(router_auth)

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
