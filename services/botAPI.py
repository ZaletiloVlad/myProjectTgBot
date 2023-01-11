import requests


class BotAPIService:

    base_url = "http://localhost:8000/api/"

    def get_user_id(self, user_info: dict) -> None:
        response = requests.post(f"{self.base_url}users/connect/", json=user_info)
        response.raise_for_status()
        return response.json()

    # def update_user(self, user_id: int, user_data: dict) -> dict:
    #     response = requests.patch(f"{self.base_url}users_/{user_id}/", json=user_data)
    #     response.raise_for_status()
    #     return response.json()


    def get_user_spaces(self, user_id: int) -> None:
        response = requests.get(f"{self.base_url}users/{user_id}/")
        response.raise_for_status()
        return response.json()

    def create_space(self, new_space_data: dict):
        response = requests.post(f"{self.base_url}spaces/space_create/", json=new_space_data)
        response.raise_for_status()
        return response.json()


    def check_availability(self):
        response = requests.get(f"{self.base_url}ping/")
        response.raise_for_status()


bot_service = BotAPIService()