from datetime import datetime


class AbstractModel:
    created: datetime

    def __init__(self, **kwargs):
        self.created = datetime.now()
        for key, value in kwargs.items():
            setattr(self, key, value)
