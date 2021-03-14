from datetime import datetime
from abc import ABC
from api.rest import Rest


class AbstractModel(ABC):
    created: datetime = datetime.now()
    resource_name: str = ''
    rest: Rest
    relations: {}

    def __init__(self, **kwargs):
        self.rest = Rest()
        for key, value in kwargs.items():
            setattr(self, key, value)

    def filter_keys(self, data: dict):
        return {k: v for k, v in data.items() if k not in {"rest", "relations", "resource_name"}}

    def serialize(self, data: dict):
        normalized_data = self.filter_keys({**self.__dict__, **data})
        # Populate IRI for object relations
        for key, value in normalized_data.items():
            if key in self.relations:
                normalized_data[key] = '/' + self.rest.api_uri + self.relations[key].resource_name + '/' + value.lower()
        print(normalized_data)

        return normalized_data

    def persist(self, data: dict = {}):
        response = self.rest.post(resource=self.resource_name, data=self.serialize(data))
        return response.json()
