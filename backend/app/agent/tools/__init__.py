from app.agent.tools.registry import registry
from app.agent.tools.restaurant_tools import register_restaurant_tools
from app.agent.tools.menu_tools import register_menu_tools
from app.agent.tools.reservation_tools import register_reservation_tools
from app.agent.tools.order_tools import register_order_tools
from app.agent.tools.user_tools import register_user_tools


def register_all_tools():
    if registry.all():
        return
    register_restaurant_tools()
    register_menu_tools()
    register_reservation_tools()
    register_order_tools()
    register_user_tools()