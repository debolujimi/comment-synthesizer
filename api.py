from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from comments_generation_wordnet_rulebased import translate_chat

app = FastAPI(title="App Comment Synthesizer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MessageRequest(BaseModel):
    message: str = Field(min_length=1, max_length=1000)


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
