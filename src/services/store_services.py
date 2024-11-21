from apis.store_manager import StoreBackendManager


async def get_items():
    api_manager = StoreBackendManager()
    items = await api_manager.get_items()
    return items