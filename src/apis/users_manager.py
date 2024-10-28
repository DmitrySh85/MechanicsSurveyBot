from settings import BACKEND_API_TOKEN, BACKEND_API_URL
from aiohttp import ClientSession
from bot_logger import init_logger
from typing import Optional


logger = init_logger(__name__)


class UsersBackendAPIManager:
    def __init__(self):
        self.backend_api_url = BACKEND_API_URL
        self.backend_api_token = BACKEND_API_TOKEN
        
    def _get_authorization_headers(self):
        headers = {"Authorization": f"Token {self.backend_api_token}"}
        return headers

    async def send_registration_request(
            self, 
            tg_id: int, 
            username: str, 
            is_blocked: Optional[bool] = False):
        url = f"{self.backend_api_url}/api/employees/"
        headers = self._get_authorization_headers()
        payload = {
            "tg_id": tg_id,
            "name": username,
            "is_blocked": is_blocked
        }
        async with ClientSession() as session:

            response = await session.post(
                url=url, json=payload, headers=headers
            )
        return response
    
    async def get_user_from_backend(
            self,
            tg_id: int, 
            is_blocked: Optional[bool] = None,
            role: Optional[str] = None
            ):
        url = f"{self.backend_api_url}/api/employees/"
        headers = self._get_authorization_headers()
        payload = {
            "tg_id": tg_id,
            }
        if is_blocked is not None:
            payload["is_blocked"] = int(is_blocked)
        if role:
            payload["role"] = role
        async with ClientSession() as session:
            response = await session.get(
                url=url, params=payload, headers=headers
            )
        data = await response.json()
        results = data.get("results")
        if results:
            return results[0]

    async def get_users_from_backend(
            self,
            role: Optional[str] = None,
            is_blocked: Optional[bool] = None
    ):
        headers = self._get_authorization_headers()
        url = f"{self.backend_api_url}/api/employees/"
        payload = {}
        if role:
            payload["role"] = role
        if is_blocked:
            payload["is_blocked"] = int(is_blocked)
        async with ClientSession() as session:
            response = await session.get(
                url=url, params=payload, headers=headers
            )
        data = await response.json()
        results = data.get("results")
        if results:
            return results
    
    async def increment_user_points(self, tg_id: int):
        user = await self.get_user_from_backend(tg_id)
        points = user.get("points")
        user["points"] = points + 1
        await self.update_user(user)

    async def set_user_is_blocked(self, tg_id: int):
        user = await self.get_user_from_backend(tg_id)
        user["is_blocked"] = True
        await self.update_user(user)

    async def update_user(self, user: dict):
        headers = self._get_authorization_headers()
        url = f"{self.backend_api_url}/api/employees/{user.get('id')}/"
        async with ClientSession() as session:
            response = await session.put(
                url=url, json=user, headers=headers
            )
            
    
    