from fastapi import FastAPI  # pyright: ignore[reportMissingImports]

app = FastAPI()

@app.get('/')
async def hello():
    return {"hello"}


       