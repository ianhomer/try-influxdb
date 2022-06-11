import os


class Config:
    def __init__(self):
        self._token = os.environ.get("INFLUX_TOKEN_MY_ORGANISATION")
        if self.token == "":
            raise Exception(
                "Please set environment variable INFLUX_TOKEN_MY_ORGANISATION"
            )

        self._organisation = "my-organisation"
        self._bucket = "my-bucket"

    @property
    def token(self) -> str:
        return self._token or ""

    @property
    def organisation(self) -> str:
        return self._organisation

    @property
    def bucket(self) -> str:
        return self._bucket
