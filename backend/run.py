#!/usr/bin/env python
import os
import sys
from app.main import app
import uvicorn

if __name__ == "__main__":
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))
    debug = os.getenv("API_DEBUG", "false").lower() == "true"
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=debug
    )
