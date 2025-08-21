import requests
from typing import List
from dataclasses import dataclass

@dataclass
class Item:
    id: int
    description: str
    day: str
    time: str
    click_number: int

class ApiClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
    
    def create_item(self, description: str, day: str, time: str, click_number: int) -> Item:
        data = {
            "description": description,
            "day": day,
            "time": time,
            "click_number": click_number
        }
        
        response = requests.post(
            f"{self.base_url}/items/",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            return Item(**response.json())
        else:
            raise Exception(f"API Error: {response.status_code} - {response.text}")
    
    def get_items(self, skip: int = 0, limit: int = 10) -> List[Item]:
        response = requests.get(
            f"{self.base_url}/items/?skip={skip}&limit={limit}"
        )
        
        if response.status_code == 200:
            return [Item(**item) for item in response.json()]
        else:
            raise Exception(f"API Error: {response.status_code} - {response.text}")