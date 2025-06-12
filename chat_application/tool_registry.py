# --- Tool Registry ---
from chat_application.functions import *

TOOL_REGISTRY = {
    "make_purchase": make_purchase,
    "order_items": order_items,
    "create_profile": create_profile,
    "get_profile": get_profile,
    "update_profile": update_profile

    # Add new tools here as needed
}