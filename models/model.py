from datetime import datetime
from abc import ABC
from api.rest import Rest
from api.utils import filter_keys


class AbstractModel(ABC):
    created: datetime = datetime.now()
    resource_name: str = ''
    rest: Rest
    relations: {}

    def __init__(self, **kwargs):
        self.rest = Rest()
        for key, value in kwargs.items():
            setattr(self, key, value)

    def serialize(self, data: dict):
        normalized_data = filter_keys(data={**self.__dict__, **data}, keys={"rest", "relations", "resource_name"})
        # Populate IRI for object relations
        for key, value in normalized_data.items():
            if key in self.relations:
                normalized_data[key] = '/' + self.rest.api_uri + self.relations[key].resource_name + '/' + value.lower()

        return normalized_data

    def populate(self, data):
        for key, value in data[0].items():
            setattr(self, key, value)

        print(self.__dict__)
        return self

    def create(self, data: dict = {}):
        return self.populate([self.rest.post(resource=self.resource_name, data=self.serialize(data)).json()])

    def read(self, data: dict):
        return self.populate(self.rest.get(resource=self.resource_name, data=self.serialize(data)).json())
