from fastapi import FastAPI
from app.db import get_conn, create_schema

app = FastAPI()

create_schema()

@app.get("/")
def default_endpoint():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT version()")
        return cur.fetchone() 

# Sample endpoints
@app.get("/foo")
def foo():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM foo ORDER BY id DESC")
        return cur.fetchall()
    
@app.get("/foo/{id}")
def one_foo(id: int):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM foo WHERE id = %s", (id,))
        return cur.fetchall()
