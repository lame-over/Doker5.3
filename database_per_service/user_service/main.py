from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2

app = FastAPI()

def get_connection():
    return psycopg2.connect(
        host="user-db",
        database="users",
        user="user",
        password="password"
    )

# User model
class User(BaseModel):
    id: int
    name: str

@app.post("/users")
def create_user(user: User):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (id INT PRIMARY KEY, name TEXT);")
    cur.execute("INSERT INTO users (id, name) VALUES (%s, %s);", (user.id, user.name))
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "User created"}

@app.get("/users")
def get_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM users;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"id": row[0], "name": row[1]} for row in rows]
