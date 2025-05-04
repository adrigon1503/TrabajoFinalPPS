from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Bienvenido a la API de Waterpolo"}

@app.get("/partidos")
def partidos():
    return [{"equipo1": "España", "equipo2": "Italia", "resultado": "10-8"}]
