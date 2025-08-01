from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    text: str
    is_done: bool=False




items = []

@app.get("/")
def root():
    return {"Hello":"World"}

# Only when it was item : str
# curl.exe -X POST -H "Content-Type: application/json" 'http://127.0.0.1:8000/items?item=apple'   
# Now with item : Item :
# curl.exe -X POST -H "Content-Type: application/json" -d '{\"text\":\"apple\"}' http://127.0.0.1:8000/items
# \ For double quotes on windows because wrongly interpreted  

@app.post("/items")
def create_item(item : Item):
    items.append(item)
    return item

# curl.exe -X GET 'http://127.0.0.1:8000/items?limit=3'
@app.get("/items", response_model=list[Item])
def list_items(limit: int=10):
    return items[0:limit]


# curl.exe -X GET http://127.0.0.1:8000/items/0

@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int) -> Item:
    if item_id<len(items):
        item = items[item_id]
    else:
        raise HTTPException(status_code=404,detail="Item not found")
    return item