import requests


class Rest:
    url = "http://localhost:3000/hello"

    payload = {"content": "shinken"}
    headers = {
        'Content-Type': 'application/json'
    }

    def makeRequest(self):
        response = requests.request(
            "POST",
            self.url,
            headers=self.headers,
            data=self.payload
        )
        print(response.text.encode('utf8'))

