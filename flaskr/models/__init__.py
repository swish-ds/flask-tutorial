from enum import unique
from typing import DefaultDict
from sqlalchemy.orm import defaultload
from flaskr import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Base(object):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)


class CreatedAtMixin(object):
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)


class TimestampMixin(object):
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

