from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/hello")
def hello():
    return {"message": "hello from ci/cd"}
