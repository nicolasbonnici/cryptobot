from api.rest import Rest


class AbstractModel(Rest):
    resource_name = ''

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)