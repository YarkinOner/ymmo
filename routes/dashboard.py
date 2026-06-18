from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy import func
from app import db
from models import Listing, Contact, User

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'client':
        from models import Favorite
        favorites = Favorite.query.filter_by(user_id=current_user.id).all()
        return render_template('dashboard_client.html', favorites=favorites)

    # Agent / Admin view
    listings = Listing.query.filter_by(user_id=current_user.id).all()
    contacts = Contact.query.join(Listing).filter(Listing.user_id == current_user.id).all()

    # Stats for chart (listings per city)
    city_stats = db.session.query(
        Listing.city, func.count(Listing.id)
    ).filter_by(status='active').group_by(Listing.city).all()

    price_stats = db.session.query(
        Listing.property_type, func.avg(Listing.price)
    ).filter_by(status='active').group_by(Listing.property_type).all()

    return render_template('dashboard_agent.html',
        listings=listings,
        contacts=contacts,
        city_stats=city_stats,
        price_stats=price_stats
    )
