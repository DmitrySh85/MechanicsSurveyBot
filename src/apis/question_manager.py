from settings import BACKEND_API_TOKEN, BACKEND_API_URL
from aiohttp import ClientSession


class QuestionsBackendManager:

    def __init__(self):
        self.backend_api_url = BACKEND_API_URL
        self.backend_api_token = BACKEND_API_TOKEN

    def _get_authorization_headers(self):
        headers = {"Authorization": f"Token {self.backend_api_token}"}
        return headers

    async def get_questions(self):
        number_of_questions = 3
        payload = {"length": number_of_questions}
        url = f"{self.backend_api_url}/api/survey/questions/"
        headers = self._get_authorization_headers()
        async with ClientSession() as session:
            response = await session.get(
                url=url, params=payload, headers=headers
            )
        data = await response.json()
        return data

