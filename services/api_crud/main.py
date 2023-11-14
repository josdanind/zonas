from fastapi import FastAPI

app = FastAPI(title="API CRUD")


@app.get("/")
def home():
    return {"from": "API CRUD Service"}
