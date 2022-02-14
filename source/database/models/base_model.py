class BaseModel:
    def get_dict(self) -> dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}