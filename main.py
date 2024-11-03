

import asyncio
import json
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
from bailianapi import BaiLianAdapter
load_dotenv()


app = FastAPI()


TASK_SESSION_ID_MAP = {}


@app.post("/chat/completions")
async def chat(request: Request):
    data = await request.json()
    messages = data.get("messages", [])

    # for trtc ai conversation
    task_id = request.headers.get("X-Task-Id")
    request_id = request.headers.get("X-Request-Id")

    session_id = None
    if task_id:
        session_id = TASK_SESSION_ID_MAP.get(task_id)

    client = BaiLianAdapter(os.getenv("DASHSCOPE_API_KEY"),
                            os.getenv("DASHSCOPE_APP_ID"))
    response = await client.create_chat_completion(messages, session_id=session_id)

    if response:
        TASK_SESSION_ID_MAP[task_id] = client.session_id

    return JSONResponse(content=response)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
