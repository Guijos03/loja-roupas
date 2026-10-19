from fastapi import FastAPI, HTTPException

from loja.produto import Calca, Camiseta, Produto

app = FastAPI(title="Loja de Roupas")

# o catálogo: cada produto ganha um número (id)
CATALOGO = {
    1: Camiseta("Camiseta básica", 39.90, "M", "curta"),
    2: Calca("Calça jeans", 129.90, "G", "reta"),
    3: Produto("Moletom", 159.90, "P"),
}


def com_id(produto_id, produto):
    return {"id": produto_id, **produto.para_dict()}


@app.get("/")
def inicio():
    return {"loja": "Loja de Roupas", "documentacao": "/docs"}


@app.get("/produtos")
def listar_produtos():
    return [com_id(i, p) for i, p in CATALOGO.items()]


@app.get("/produtos/{produto_id}")
def buscar_produto(produto_id: int):
    if produto_id not in CATALOGO:
        raise HTTPException(status_code=404, detail="produto não encontrado")
    return com_id(produto_id, CATALOGO[produto_id])