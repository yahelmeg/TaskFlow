from fastapi import FastAPI
from backend.database import create_tables, initialize_roles_and_permissions, delete_database
import uvicorn

app = FastAPI()

#delete_database()
create_tables()
initialize_roles_and_permissions()

@app.get("/")
def read_root():
    return {"message": "Welcome to TaskFlow API!"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)