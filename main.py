import sys
import uvicorn
from fastapi import FastAPI

port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
app = FastAPI()


@app.get("/")
def read_root():
    return {"message": f"Hello, World! from port: {port}"}


uvicorn.run(app, host="0.0.0.0", port=port)
