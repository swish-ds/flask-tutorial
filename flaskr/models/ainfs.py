from sqlalchemy import JSON, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from flaskr import db
from . import Base, CreatedAtMixin, TimestampMixin

# CREATE TABLE post (
#   id INTEGER PRIMARY KEY AUTOINCREMENT,
#   created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
#   title TEXT NOT NULL,
#   body TEXT NOT NULL
# );


class Zones(CreatedAtMixin, Base, db.Model):
    name = db.Column(db.String(50), nullable=False, unique=True)

    jobs = relationship("Jobs", back_populates='zone_info', lazy='joined')


class Jobs(TimestampMixin, Base, db.Model):
    __table_args__ = (UniqueConstraint('name', 'zone_id', name='unique_job'),)
    project_path = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    config = db.Column(db.String(50), nullable=False)

    zone_id = db.Column(UUID(as_uuid=True), db.ForeignKey('zones.id', ondelete='CASCADE'), nullable=False)
    zone_info = relationship("Zones", back_populates='jobs')


class Post(CreatedAtMixin, Base, db.Model):
    title = db.Column(db.String(50), nullable=False, unique=True)
    body = db.Column(db.String(), nullable=False)
