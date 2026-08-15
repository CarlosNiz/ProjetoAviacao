from fastapi import FastAPI

app = FastAPI(title="Engemap API");

@app.get("/saude")
def verificar_saude() -> dict[str, str]:
    return {"status": "ok"}