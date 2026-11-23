
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

AI_ENGINE_URL = "http://127.0.0.1:8001/analyze"


def analyze_with_ai(data):
    payload = json.dumps(data).encode("utf-8")

    request = Request(
        AI_ENGINE_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urlopen(request, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))

    except HTTPError as error:
        details = error.read().decode("utf-8")
        raise RuntimeError(f"AI Engine Error: {details}")

    except URLError as error:
        raise RuntimeError(f"AI Engine Connection Failed: {error}")

    except TimeoutError:
        raise RuntimeError("AI Engine request timed out")
