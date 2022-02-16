from .. import Session
from ..models.base_model import BaseModel


class BaseMethod:
    def __init__(self, c_type, session: Session = Session()):
        self.type = c_type
        self.session = session

    def get(self, **kwargs) -> list:
        return [x for x in self.session.query(self.type).filter_by(**kwargs)]

    def exists(self, **kwargs) -> bool:
        return bool([x for x in self.session.query(self.type).filter_by(**kwargs)])

    def add(self, c_object: BaseModel):
        if not isinstance(c_object, self.type):
            raise TypeError(f'Invalid type. Wanted: {self.type}, Got: {c_object.__class__}')

        try:
            self.session.add(c_object)
            self.session.commit()
        except Exception as e:
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

    def update(self, c_object: BaseModel):
        if not isinstance(c_object, self.type):
            raise TypeError(f'Invalid type. Wanted: {self.type}, Got: {c_object.__class__}')

        try:
            self.session.commit()
            return c_object
        except:
            self.session.rollback()
            return None
