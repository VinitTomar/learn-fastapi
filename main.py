from enum import Enum

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

fake_items_db = [
    { "item_name": "Foo" },
    { "item_name": "Bar" },
    { "item_name": "Baz" },
]

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None


@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]

@app.post("/items/")
async def create_item(item: Item):
    return item


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}

    if q:
        item.update({ "q": q })
    
    if not short:
        item.update(
            {
                "description": "This is an amazing item with a long description."
            }
        )

    return item

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {
        "item_id": item_id,
        **item.model_dump()
    }


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    
    return {"model_name": model_name, "message": "Have some residuals"}