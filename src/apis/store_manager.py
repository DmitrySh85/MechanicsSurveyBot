from settings import BACKEND_API_TOKEN, BACKEND_API_URL
from aiohttp import ClientSession, ClientResponse
from uuid import UUID


class StoreBackendManager:

    def __init__(self):
        self.backend_api_url = BACKEND_API_URL
        self.backend_api_token = BACKEND_API_TOKEN

    def _get_authorization_headers(self):
        headers = {"Authorization": f"Token {self.backend_api_token}"}
        return headers

    async def get_items(self):
        url = f"{self.backend_api_url}/api/store/items/"
        headers = self._get_authorization_headers()
        async with ClientSession() as session:
            response = await session.get(url=url, headers=headers)
            items = await response.json()
            return items
        
    async def create_order(self, user_id: UUID, item_id: int) -> ClientResponse:
        url = f"{self.backend_api_url}/api/store/order/"
        headers = self._get_authorization_headers()
        payload = {
            "purchaser": user_id,
            "item": item_id
        }
        async with ClientSession() as session:
            response = await session.post(url=url, json=payload, headers=headers)
            return response