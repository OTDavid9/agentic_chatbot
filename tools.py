tools = [{
        "type": "function",
        "function": {
            "name": "make_purchase",
            "description": "This function is meant to make purchase of items ",
            "parameters": {
                "type": "object",
                "properties": {
                    "item_name": {"type": "string"}
                },
                "required": ["item_name"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "order_items",
            "description": "This function is meant to make order of items ",
            "parameters": {
                "type": "object",
                "properties": {
                    "item_name": {"type": "string"},
                    "quantity": {"type": "integer"},

                },
                "required": ["item_name", "quantity"]
            }
        }
    }

]