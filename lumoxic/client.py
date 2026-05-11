import os
import json
import urllib.request
import urllib.parse
from dataclasses import dataclass
from typing import Optional


@dataclass
class OptimizationResult:
    status: str
    before: dict
    after: dict
    delta: dict
    download_url: str
    job_id: str

    @property
    def summary(self) -> str:
        d = self.delta
        return f"{d.get('size_reduction','')} smaller | {d.get('speedup','')} faster | {d.get('size_saved_pct','')} saved"

    def download(self, path: str) -> str:
        urllib.request.urlretrieve(self.download_url, path)
        return path


class Client:
    BASE_URL = "https://api.lumoxicai.me/v1"

    def __init__(self, api_key: str, base_url: Optional[str] = None):
        self.api_key = api_key
        if base_url:
            self.BASE_URL = base_url

    def optimize(self, model: str, target: str = "server", strategy: str = "auto") -> OptimizationResult:
        if not os.path.exists(model):
            raise FileNotFoundError(f"Model not found: {model}")

        boundary = "----LumoxicBoundary"
        filename = os.path.basename(model)
        with open(model, "rb") as f:
            model_data = f.read()

        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="model"; filename="{filename}"\r\n'
            f"Content-Type: application/octet-stream\r\n\r\n"
        ).encode() + model_data + (
            f"\r\n--{boundary}\r\n"
            f'Content-Disposition: form-data; name="strategy"\r\n\r\n{strategy}\r\n'
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="target"\r\n\r\n{target}\r\n'
            f"--{boundary}--\r\n"
        ).encode()

        req = urllib.request.Request(
            f"{self.BASE_URL}/optimize",
            data=body,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": f"multipart/form-data; boundary={boundary}",
            },
        )

        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())

        return OptimizationResult(
            status=data["status"],
            before=data["before"],
            after=data["after"],
            delta=data["delta"],
            download_url=data.get("download_url", ""),
            job_id=data.get("job_id", ""),
        )

    def benchmark(self, model: str) -> dict:
        with open(model, "rb") as f:
            model_data = f.read()
        boundary = "----LumoxicBoundary"
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="model"; filename="{os.path.basename(model)}"\r\n'
            f"Content-Type: application/octet-stream\r\n\r\n"
        ).encode() + model_data + f"\r\n--{boundary}--\r\n".encode()

        req = urllib.request.Request(
            f"{self.BASE_URL}/benchmark",
            data=body,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": f"multipart/form-data; boundary={boundary}",
            },
        )
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())

    def usage(self) -> dict:
        req = urllib.request.Request(
            f"{self.BASE_URL}/usage",
            headers={"Authorization": f"Bearer {self.api_key}"},
        )
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())