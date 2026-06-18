from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from datetime import datetime

db = SQLAlchemy()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Agency(db.Model):
    __tablename__ = 'agencies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100))
    address = db.Column(db.String(200))
    users = db.relationship('User', backref='agency', lazy=True)
    listings = db.relationship('Listing', backref='agency', lazy=True)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='client')
    agency_id = db.Column(db.Integer, db.ForeignKey('agencies.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    listings = db.relationship('Listing', backref='agent', lazy=True)
    favorites = db.relationship('Favorite', backref='user', lazy=True)

class Listing(db.Model):
    __tablename__ = 'listings'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(20))
    property_type = db.Column(db.String(30))
    status = db.Column(db.String(20), default='active')
    price = db.Column(db.Float, nullable=False)
    area_m2 = db.Column(db.Integer)
    rooms = db.Column(db.Integer)
    city = db.Column(db.String(100))
    address = db.Column(db.String(200))
    description = db.Column(db.Text)
    agency_id = db.Column(db.Integer, db.ForeignKey('agencies.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    images = db.relationship('ListingImage', backref='listing', lazy=True, cascade='all, delete-orphan')
    contacts = db.relationship('Contact', backref='listing', lazy=True)

class ListingImage(db.Model):
    __tablename__ = 'listing_images'
    id = db.Column(db.Integer, primary_key=True)
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'), nullable=False)
    url = db.Column(db.String(300))

class Favorite(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'), nullable=False)
    listing = db.relationship('Listing')

class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'), nullable=False)
    message = db.Column(db.Text)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User')