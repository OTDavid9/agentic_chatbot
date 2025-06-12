tools = [
    {
        "type": "function",
        "name": "order_items",
        "description": "Fetch details about products, including price, availability, and specifications.",
        "parameters": {
            "type": "object",
            "properties": {
                "product_name": {
                    "type": "string",
                    "description": "The name of the product to search for."
                }
            },
            "required": ["product_name"],
            "additionalProperties": False
        }
    },
    {
        "type": "function",
        "name": "make_purchase",
        "description": "Process a purchase order after the user confirms the product details.",
        "parameters": {
            "type": "object",
            "properties": {
                "product_name": {
                    "type": "string",
                    "description": "The name of the product to purchase."
                },
                "quantity": {
                    "type": "integer",
                    "description": "The number of units the user wants to purchase."
                },
                "price": {
                    "type": "number",
                    "description": "The total price of the product(s) to charge the user."
                }
            },
            "required": ["product_name", "quantity", "price"],
            "additionalProperties": False
        }
    },
    {
        "type": "function",
        "name": "create_profile",
        "description": "Create a new user profile.",
        "parameters": {
            "type": "object",
            "properties": {
                "username": {
                    "type": "string",
                    "description": "A unique username for the user."
                },
                "name": {
                    "type": "string",
                    "description": "The user's full name."
                },
                "email": {
                    "type": "string",
                    "description": "The user's email address."
                },
                "age": {
                    "type": "integer",
                    "description": "The user's age."
                }
            },
            "required": ["username", "name", "email", "age"],
            "additionalProperties": False
        }
    },
    {
        "type": "function",
        "name": "get_profile",
        "description": "Retrieve an existing user profile using the username.",
        "parameters": {
            "type": "object",
            "properties": {
                "username": {
                    "type": "string",
                    "description": "The username of the profile to retrieve."
                }
            },
            "required": ["username"],
            "additionalProperties": False
        }
    },
    {
        "type": "function",
        "name": "update_profile",
        "description": "Update an existing user's profile.",
        "parameters": {
            "type": "object",
            "properties": {
                "username": {
                    "type": "string",
                    "description": "The username of the profile to update."
                },
                "name": {
                    "type": "string",
                    "description": "The user's full name."
                },
                "email": {
                    "type": "string",
                    "description": "The user's email address."
                },
                "age": {
                    "type": "integer",
                    "description": "The user's age."
                }
            },
            "required": ["username", "name", "email", "age"],
            "additionalProperties": False
        }
    }
]

ollama_tools = [
    {
        "type": "function",
        "function": {
            "name": "create_profile",
            "description": "Create a new user profile.",
            "parameters": {
                "type": "object",
                "properties": {
                    "username": {"type": "string", "description": "Unique username of the user."},
                    "name": {"type": "string", "description": "Full name of the user."},
                    "email": {"type": "string", "description": "Email address of the user."},
                    "age": {"type": "integer", "description": "Age of the user."}
                },
                "required": ["username", "name", "email", "age"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_profile",
            "description": "Retrieve an existing user profile by username.",
            "parameters": {
                "type": "object",
                "properties": {
                    "username": {"type": "string", "description": "Unique username of the user."}
                },
                "required": ["username"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_profile",
            "description": "Update an existing user profile.",
            "parameters": {
                "type": "object",
                "properties": {
                    "username": {"type": "string", "description": "Unique username of the user."},
                    "name": {"type": "string", "description": "Full name of the user."},
                    "email": {"type": "string", "description": "Email address of the user."},
                    "age": {"type": "integer", "description": "Age of the user."}
                },
                "required": ["username", "name", "email", "age"]
            }
        }
    },
{
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

