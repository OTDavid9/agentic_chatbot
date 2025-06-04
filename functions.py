def make_purchase(item_name:str):
    return {"message": f"{item_name} was purchased!"}

def order_items(item_name:str, quantity:int):
    return {"message": f"{quantity} {item_name} were ordered!"}