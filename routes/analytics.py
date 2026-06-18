from flask import Blueprint, render_template, jsonify
from sqlalchemy import func
from models import db, Listing

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/analytics')
def analytics():
    return render_template('analytics.html')

@analytics_bp.route('/api/analytics')
def analytics_data():
    # 1. Annonces par ville
    city_data = db.session.query(
        Listing.city, func.count(Listing.id)
    ).filter_by(status='active').group_by(Listing.city).all()

    # 2. Prix moyen par type de bien
    price_by_type = db.session.query(
        Listing.property_type, func.avg(Listing.price), func.count(Listing.id)
    ).filter_by(status='active').group_by(Listing.property_type).all()

    # 3. Distribution vente vs location
    type_dist = db.session.query(
        Listing.type, func.count(Listing.id)
    ).group_by(Listing.type).all()

    # 4. Prix moyen par ville
    price_by_city = db.session.query(
        Listing.city, func.avg(Listing.price), func.avg(Listing.area_m2)
    ).filter_by(status='active').group_by(Listing.city).all()

    # 5. Prix au m2 par ville
    listings_raw = Listing.query.filter(
        Listing.area_m2 > 0, Listing.status == 'active'
    ).all()
    price_per_m2 = {}
    for l in listings_raw:
        if l.city not in price_per_m2:
            price_per_m2[l.city] = []
        price_per_m2[l.city].append(l.price / l.area_m2)
    price_m2_avg = {city: round(sum(v)/len(v)) for city, v in price_per_m2.items()}

    return jsonify({
        'city_counts': [{'city': r[0], 'count': r[1]} for r in city_data],
        'price_by_type': [{'type': r[0], 'avg_price': round(r[1]), 'count': r[2]} for r in price_by_type],
        'type_dist': [{'type': r[0], 'count': r[1]} for r in type_dist],
        'price_by_city': [{'city': r[0], 'avg_price': round(r[1]), 'avg_area': round(r[2])} for r in price_by_city],
        'price_per_m2': [{'city': k, 'price_m2': v} for k, v in price_m2_avg.items()],
        'total_listings': Listing.query.filter_by(status='active').count(),
        'avg_price': round(db.session.query(func.avg(Listing.price)).filter_by(status='active').scalar() or 0),
        'avg_area': round(db.session.query(func.avg(Listing.area_m2)).filter_by(status='active').scalar() or 0),
    })