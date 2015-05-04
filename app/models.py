from datetime import date as dt
from flask.ext.login import UserMixin
from simplecrypt import encrypt
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from app import db, login_manager
from config import SECRET_KEY

########################
# Tables
########################

participants = db.Table('participants',
		db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
		db.Column('event_id', db.Integer, db.ForeignKey('event.id')))

########################
# Models
########################

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64))
	email = db.Column(db.String(128), unique=True)
	password = db.Column(db.LargeBinary(4096))

	#Metadata tags useful for filtering
	metadata_str = db.Column(db.LargeBinary(4096))
	wins = db.Column(db.Integer)
	losses = db.Column(db.Integer)
	ties = db.Column(db.Integer)
	total_played = db.Column(db.Integer)
	events_played = db.relationship('Event', secondary=participants, backref=db.backref("events", lazy="dynamic"))

	def __init__(self, name):
		self.name = name
		self.password = ""
		self.metadata_str = ""
		self.wins = 0
		self.losses = 0
		self.ties = 0
		self.total_played = self.wins+self.losses+self.ties

	@hybrid_method
	def initialize(self, email, password):
		self.email = email
		self.password = encrypt(SECRET_KEY, password)
		db.session.commit()

	@hybrid_property
	def get_metadata(self):
		return self.metadata.split("\t")

	@hybrid_method
	def set_metadata(self):
		self.metadata = '\t'.join(metadata)

	def __repr__(self):
		return '<User %r>' % (self.name)

class Event(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64))
	event_type = db.Column(db.String(64))
	datetime = db.Column(db.DateTime)
	description = db.Column(db.String(256))
	host = db.Column(db.String(64))
	participants = db.relationship('User', secondary=participants, backref=db.backref("users", lazy="dynamic"))
	winner = db.Column(db.String(64))

	def __init__(self, event_name, datetime, event_type, host, description, participants, winner=None, loser=None, draw=False):
		self.name = event_name
		self.datetime = datetime
		self.winner = winner
		self.loser = loser
		self.event_type = event_type
		self.results = dict()
		self.host = host
		self.description = description

	def __repr__(self):
		return '<%r on %r>' % (self.name, self.datetime.strftime("%Y-%m-%d %H:%M:%S"))


########################
# Helper Functions
########################

@login_manager.user_loader
def get_user(id=None, name=None, email=None):
	if id:
		return User.query.filter_by(id=int(id)).first()
	if name:
		return User.query.filter_by(name=name).first()
	if email:
		return User.query.filter_by(email=email).first()
	return None

def get_events(name=None):
	if name:
		#print len(Event.query.filter_by(host=name).all())
		return Event.query.filter_by(host=name).all()
	return None

def get_event(id=None, datetime=None):
	if id:
		return Event.query.filter_by(id=int(id)).first()
	if datetime:
		return Event.query.filter_by(datetime=datetime).first()


def record_result(event, datetime, event_type, host, winner, loser, draw=False):
	e = Event(event, datetime, winner, loser, draw, event_type, host)
	if draw:
		User(winner).record['ties'] += 1
		User(loser).record['ties'] += 1
	else:
		User(winner).record['wins'] += 1
		User(loser).record['losses'] += 1
	User(winner).events_played.append(e)
	db.session.commit()
	return e

