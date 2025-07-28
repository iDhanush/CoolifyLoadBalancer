from fastapi import FastAPI
import sys
import uvicorn

port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
app = FastAPI()


@app.get("/")
def read_root():
    return {"message": f"Hello, World! {port}"}


uvicorn.run("main:app", host="0.0.0.0", port=port)
