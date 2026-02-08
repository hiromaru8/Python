import json
import urllib.request
import urllib.error


class APIClient:
    def __init__(self, base_url, timeout=5):
        self.base_url = base_url
        self.timeout = timeout

    def get(self, path):
        url = self.base_url + path
        try:
            with urllib.request.urlopen(url, timeout=self.timeout) as response:
                return json.loads(response.read().decode())
        except urllib.error.HTTPError as e:
            return {"error": str(e)}
        except Exception as e:
            return {"error": str(e)}
