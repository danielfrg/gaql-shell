from typing import Optional

from adsctl import client
from adsctl.config.config_file import ConfigFile
from adsctl.config.model import RootConfig
from adsctl.parse import parseStream


class Application:
    config_file: ConfigFile
    client = None
    _customer_id: Optional[str]

    def __init__(self, config_file=None, customer_id=None, create_client=True):
        self.config_file = config_file or ConfigFile()
        self.config_file.load()
        self._customer_id = customer_id or self.config_file.model.customer_id

        if create_client:
            self.create_client()

    @property
    def config(self) -> RootConfig:
        return self.config_file.model

    @property
    def customer_id(self) -> str | None:
        if self._customer_id is not None:
            return self._customer_id.replace("-", "")

    @customer_id.setter
    def customer_id_set(self, value: str | None):
        if value is not None:
            self._customer_id = value

    def create_client(self):
        if self.client is None:
            gads_config = self.config_file.model.clientSettings()
            self.client = client.get_client(gads_config)

    def search_stream(self, query):
        customer_id = self.config_file.model.customer_id
        stream = client.search_stream(query, self.client, customer_id)
        return stream

    def query(self, query):
        stream = self.search_stream(query)
        tables = parseStream(stream)
        return tables


# Alias
GoogleAds = Application