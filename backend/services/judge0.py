
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

JUDGE0_API_URL = os.getenv("JUDGE0_API_URL", "https://ce.judge0.com")
JUDGE0_API_KEY = os.getenv("JUDGE0_API_KEY", "")

JAVA_LANGUAGE_ID = 91


def submit_code(source_code, stdin=""):
    url = f"{JUDGE0_API_URL}/submissions"

    headers = {
        "Content-Type": "application/json"
    }

    if JUDGE0_API_KEY:
        headers["X-Auth-Token"] = JUDGE0_API_KEY

    payload = {
        "language_id": JAVA_LANGUAGE_ID,
        "source_code": source_code,
        "stdin": stdin
    }

    response = requests.post(
        url,
        params={"base64_encoded": "false", "wait": "false"},
        json=payload,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()
    return response.json()["token"]


def get_submission_result(token):
    url = f"{JUDGE0_API_URL}/submissions/{token}"

    headers = {}

    if JUDGE0_API_KEY:
        headers["X-Auth-Token"] = JUDGE0_API_KEY

    for _ in range(30):
        response = requests.get(
            url,
            params={"base64_encoded": "false"},
            headers=headers,
            timeout=30
        )

        response.raise_for_status()
        result = response.json()

        status_id = result["status"]["id"]

        if status_id not in (1, 2):
            return result

        time.sleep(1)

    raise TimeoutError("Judge0 execution timed out")
