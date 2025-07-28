import sys
import time
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import uvicorn
from starlette.status import HTTP_206_PARTIAL_CONTENT

port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
serial = int(sys.argv[2]) if len(sys.argv) > 2 else 0
app = FastAPI()


@app.get("/")
def read_root():
    return {"message": f"Hello, World! from port: {port}"}


@app.get("/speed")
async def download_speed(request: Request):
    chunk_size = 1024 * 1024  # 1 MB
    total_size = 4 * 1024 * chunk_size  # 1 GB in bytes

    range_header = request.headers.get("range")
    start = 0
    end = total_size - 1  # Byte range

    if range_header:
        # Parse range: bytes=start-end
        match = range_header.strip().lower().replace("bytes=", "").split("-")
        start = int(match[0]) if match[0] else 0
        end = int(match[1]) if len(match) > 1 and match[1] else total_size - 1

    async def file_generator(start_pos, end_pos):
        current = start_pos
        while current <= end_pos:
            remaining = end_pos - current + 1
            size = min(chunk_size, remaining)
            yield b"0" * size
            current += size

    content_length = end - start + 1

    headers = {
        "Content-Type": "application/octet-stream",
        "Content-Disposition": f"attachment; filename=test_4GB.dat",
        "Accept-Ranges": "bytes",
        "Content-Range": f"bytes {start}-{end}/{total_size}",
        "Content-Length": str(content_length)
    }

    return StreamingResponse(
        file_generator(start, end),
        status_code=HTTP_206_PARTIAL_CONTENT if range_header else 200,
        headers=headers,
    )


# time.sleep(serial * 100)
uvicorn.run(app, host="0.0.0.0", port=port)
