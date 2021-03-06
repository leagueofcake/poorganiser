#!/usr/bin/env python3.5
from config import porg_config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DbInterface():
    """Main class for handling database interfacing."""

    def __init__(self):
        self._engine = create_engine(porg_config.DB_URL)
        self.s = sessionmaker(bind=self._engine)()

    def _get_by_id(self, obj_id, obj_type):
        """Returns an object in the database with matching object id and object type."""
        if obj_id:
            return self.s.query(obj_type).get(obj_id)

    def get_obj(self, obj, obj_type):
        """Given obj (usually id or Object), returns corresponding object within the database.
        Usually used when a function can take either an Object id or an Object."""
        if isinstance(obj, obj_type):
            return self._get_by_id(obj.get_id(), obj_type)
        else:
            return self._get_by_id(obj, obj_type)

    def query(self, obj_type, filter, num='one'):
        res = self.s.query(obj_type).filter(filter)
        if num == 'one':
            return res.first()
        elif num == 'all':
            return res.all()

    def add(self, obj):
        """Inserts given object to the database."""
        self.s.add(obj)
        self.s.commit()

    def update(self, obj):
        """commits any changes done on obj to the database and performs any pre-commit processing
        (such as list object to string conversion).

        Returns obj."""

        self.s.commit()
        return obj

    def delete(self, obj):
        self.s.delete(obj)
        self.s.commit()
