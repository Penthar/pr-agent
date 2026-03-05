import requests
import time
import socket


class SplunkHECSink:
    def __init__(self, url: str, token: str, sourcetype="pr-agent"):
        self.url = url.rstrip("/") + "/services/collector/event"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Splunk {token}",
            "Content-Type": "application/json"
        })
        self.sourcetype = sourcetype
        self.host = socket.gethostname()

    def write(self, message):
        record = message.record

        payload = {
            "time": time.time(),
            "host": self.host,
            "sourcetype": self.sourcetype,
            "event": {
                "level": record["level"].name,
                "message": record["message"],
                **record["extra"],
            },
        }

        try:
            self.session.post(self.url, json=payload, timeout=2)
        except Exception:
            # never break the app because of logging
            pass