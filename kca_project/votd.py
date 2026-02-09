import requests

def get_votd():
    url = "https://beta.ourmanna.com/api/v1/get?format=json&order=daily"
    headers = {"accept": "application/json"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            return response.json()
    except requests.RequestException:
        pass
    return None