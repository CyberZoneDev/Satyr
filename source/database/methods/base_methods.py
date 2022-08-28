from typing import Optional, Any, List

from .. import Session
from ..models.base_model import BaseModel


class BaseMethod:
    def __init__(self, c_type, session: Session = Session()):
        self.type = c_type
        self.session = session

    def get(self, ready=True, **kwargs) -> Any:
        query = self.session.query(self.type).filter_by(**kwargs)
        return [x for x in query] if ready else query

    def exists(self, **kwargs) -> bool:
        return bool(self.get(**kwargs))

    def add(self, c_object: BaseModel, **kwargs) -> Optional[BaseModel]:
        if not isinstance(c_object, self.type):
            raise TypeError(f'Invalid type. Wanted: {self.type}, Got: {c_object.__class__}')

        try:
            self.session.add(c_object)
            self.session.commit()
        except:
            self.session.rollback()
            return None

        return c_object

    def delete(self, c_object: BaseModel) -> bool:
        if not isinstance(c_object, self.type):
            raise TypeError(f'Invalid type. Wanted: {self.type}, Got: {c_object.__class__}')

        try:
            self.session.delete(c_object)
            self.session.commit()
            return True
        except:
            self.session.rollback()
            return False

    def delete_range(self, c_objects: List[BaseModel]) -> bool:
        if not c_objects:
            return False

        for i, item in enumerate(c_objects):
            if not isinstance(item, self.type):
                raise TypeError(f'Invalid type. Wanted: {self.type}, Got: {item.__class__} at index {i}')

        try:
            for item in c_objects:
                self.session.delete(item)
            self.session.commit()
            return True
        except:
            self.session.rollback()
            return False

    def update(self, c_object: BaseModel) -> Optional[BaseModel]:
        if not isinstance(c_object, self.type):
            raise TypeError(f'Invalid type. Wanted: {self.type}, Got: {c_object.__class__}')

        try:
            self.session.commit()
            return c_object
        except:
            self.session.rollback()
            return None
