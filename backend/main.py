from fastapi import FastAPI

app = FastAPI(
    title="Enterprise AI Operating System",
    description="AI platform with RAG and autonomous agents",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Enterprise AI Operating System is running"
    }