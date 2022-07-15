import logging
import time
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
from typing import Optional, Union
from pydantic import BaseModel
from fastapi import FastAPI, Response, status, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
import os


app = FastAPI()

while True:
  try:
    print("Connecting to database...")
    conn = psycopg2.connect(
      host=os.environ['DB_HOST'],
      database=os.environ['DB_NAME'],
      user=os.environ['DB_USER'],
      password=os.environ['DB_PASSWORD'],
      cursor_factory=RealDictCursor
    )
    cursor = conn.cursor()
    print('Connected to database')
    break
  except Exception as e:
    print(e)
    print('Failed to connect to database')
    time.sleep(5)
    

class Item (BaseModel):
    title: str
    content: str
    publish: bool = False
    rating: Optional[int] = None

items = []

@app.get("/items")
def get_items():
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    return {"items": items}

@app.get("/items/{id}")
def get_item(id, response: Response):
  cursor.execute("SELECT * FROM items WHERE id = %s", (id,))
  item = cursor.fetchone()
  if item is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item id:{id} not found")
  return {"item": item}

@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
  cursor.execute("""
    INSERT INTO items (title, content, publish, rating) VALUES (%s, %s, %s, %s) RETURNING *""", 
    (item.title, item.content, item.publish, item.rating))

  new_item = cursor.fetchone()
  conn.commit()
  return {"item": new_item}

@app.delete("/items/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(id: int, response: Response):
  cursor.execute("DELETE FROM items WHERE id = %s RETURNING *", (id,))
  deleted_item = cursor.fetchone()
  conn.commit()
  if deleted_item is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item id:{id} not found")
  
  return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/items/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_item(id: int, new_item: Item, response: Response):
  cursor.execute(
    """update items set title = %s, content = %s, publish = %s, rating = %s WHERE id = %s RETURNING *""", 
    (new_item.title, new_item.content, new_item.publish, new_item.rating, id))
  updated_item = cursor.fetchone()
  conn.commit()
  if updated_item is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item id:{id} found")
  return {"item": updated_item}