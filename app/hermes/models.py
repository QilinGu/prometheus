# from __future__ import print_function
import savalidation.validators as val

from datetime import datetime as dt, date as d

from app import db
from savalidation import ValidationMixin
from flask.ext.sqlalchemy import SQLAlchemy
# from sqlalchemy.schema import UniqueConstraint

class EventType(db.Model, ValidationMixin):
	__table_args__ = (db.UniqueConstraint('name', 'unit'), {})
	id = db.Column(db.Integer, primary_key=True)
	utc_created = db.Column(db.DateTime, nullable=False, default=dt.utcnow())
	utc_updated = db.Column(db.DateTime, nullable=False, default=dt.utcnow(),
		onupdate=dt.utcnow())

	name = db.Column(db.String(64), nullable=False, unique=True)
	unit = db.Column(db.String(32), nullable=False, default='USD')

	# validation
	val.validates_constraints()

	def __init__(self, name=None, unit=None):
		self.name = name
		self.unit = unit

	def __repr__(self):
		return '<Type(%r, %r)>' % (self.name, self.unit)

class Event(db.Model, ValidationMixin):
	__table_args__ = (db.UniqueConstraint('symbol', 'date', 'event_type_id',
		'value'), {})

	id = db.Column(db.Integer, primary_key=True)
	utc_created = db.Column(db.DateTime, nullable=False, default=dt.utcnow())
	utc_updated = db.Column(db.DateTime, nullable=False, default=dt.utcnow(),
		onupdate=dt.utcnow())

	symbol = db.Column(db.String(12), nullable=False)
	value = db.Column(db.Float, nullable=False)
	event_type_id = db.Column(db.Integer, db.ForeignKey('event_type.id'))
	type = db.relationship('EventType', backref='events', lazy='joined')
	date = db.Column(db.Date, nullable=False, default=d.today())

	# validation
	val.validates_constraints()

	def __init__(self, symbol=None, value=None, type=None, event_type_id=None,
		date=None):

		self.symbol = symbol
		self.value = value
		self.event_type_id = event_type_id
		self.type = type
		self.date = (date or d.today())

	def __repr__(self):
		return ('<Event(%r, %r, %r, %r)>'
			% (self.symbol, self.value, self.event_type_id, self.date))