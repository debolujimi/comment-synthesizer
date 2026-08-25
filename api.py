from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from comments_generation_wordnet_rulebased import translate_chat

app = FastAPI(title="App Comment Synthesizer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MessageRequest(BaseModel):
    message: str


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/respond")
def respond_to_message(payload: MessageRequest):
    response = translate_chat(payload.message)
    return {"response": response}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
