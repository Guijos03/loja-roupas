from fastapi import FastAPI

app = FastAPI(title="Loja de Roupas")


@app.get("/")
def inicio():
    return {"loja": "Loja de Roupas", "documentacao": "/docs"}