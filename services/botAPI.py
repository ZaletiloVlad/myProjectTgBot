import requests


class BotAPIService:

    base_url = "http://localhost:8000/api/"

    def get_user_id(self, user_info: dict) -> None:
        response = requests.post(f"{self.base_url}users/connect/", json=user_info)
        response.raise_for_status()
        return response.json()

    def update_user(self, user_data: dict) -> dict:
        response = requests.patch(f"{self.base_url}users/update_user/", json=user_data)
        response.raise_for_status()
        return response.json()

    def ban_user(self, ban_user_data: dict) -> dict:
        response = requests.patch(f"{self.base_url}users/ban_user/", json=ban_user_data)
        response.raise_for_status()
        return response.json()

    def delete_space(self, delete_space_data: dict) -> dict:
        response = requests.delete(f"{self.base_url}spaces/delete_space/", json=delete_space_data)
        response.raise_for_status()
        return response.json()

    def delete_me_from_space(self, delete_me_data: dict) -> dict:
        response = requests.delete(f"{self.base_url}spaces/delete_user/", json=delete_me_data)
        response.raise_for_status()
        return response.json()

    def delete_category(self, delete_category_data: dict) -> dict:
        response = requests.delete(f"{self.base_url}categories/delete_category/", json=delete_category_data)
        response.raise_for_status()
        return response.json()

    def get_user_spaces(self, user_id: int) -> None:
        response = requests.get(f"{self.base_url}users/{user_id}/")
        response.raise_for_status()
        return response.json()

    def get_space_info(self, space_title: dict) -> None:
        response = requests.post(f"{self.base_url}spaces/get_space_info/", json=space_title)
        response.raise_for_status()
        return response.json()

    def get_expenses_history(self, expenses_info: dict) -> None:
        response = requests.post(f"{self.base_url}expenses/get_expenses_history/", json=expenses_info)
        response.raise_for_status()
        return response.json()

    def get_categories(self, categories_info: dict) -> None:
        response = requests.post(f"{self.base_url}categories/show_categories/", json=categories_info)
        response.raise_for_status()
        return response.json()

    def create_space(self, new_space_data: dict):
        response = requests.post(f"{self.base_url}spaces/space_create/", json=new_space_data)
        response.raise_for_status()
        return response.json()

    def create_spending(self, spending_data: dict):
        response = requests.post(f"{self.base_url}expenses/make_spending/", json=spending_data)
        response.raise_for_status()
        return response.json()

    def create_category(self, new_category_data: dict):
        response = requests.post(f"{self.base_url}categories/category_create/", json=new_category_data)
        response.raise_for_status()
        return response.json()

    def join_space(self, join_space_data: dict):
        response = requests.post(f"{self.base_url}codes/join_space/", json=join_space_data)
        response.raise_for_status()
        return response.json()

    def generate_code(self, code_info: dict):
        response = requests.post(f"{self.base_url}codes/generate_code/", json=code_info)
        response.raise_for_status()
        return response.json()

    def check_availability(self):
        response = requests.get(f"{self.base_url}ping/")
        response.raise_for_status()


bot_service = BotAPIService()