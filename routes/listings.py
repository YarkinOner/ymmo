from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from models import Listing, Favorite, Contact

listings_bp = Blueprint('listings', __name__)

@listings_bp.route('/')
def index():
    q = request.args.get('q', '')
    city = request.args.get('city', '')
    type_ = request.args.get('type', '')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)

    listings = Listing.query.filter_by(status='active')
    if q:
        listings = listings.filter(Listing.title.ilike(f'%{q}%'))
    if city:
        listings = listings.filter(Listing.city.ilike(f'%{city}%'))
    if type_:
        listings = listings.filter_by(type=type_)
    if min_price:
        listings = listings.filter(Listing.price >= min_price)
    if max_price:
        listings = listings.filter(Listing.price <= max_price)

    listings = listings.order_by(Listing.created_at.desc()).all()
    return render_template('index.html', listings=listings)

@listings_bp.route('/listing/<int:id>')
def detail(id):
    listing = Listing.query.get_or_404(id)
    return render_template('detail.html', listing=listing)

@listings_bp.route('/listing/new', methods=['GET', 'POST'])
@login_required
def new_listing():
    if current_user.role not in ('agent', 'admin'):
        flash('Accès refusé.', 'danger')
        return redirect(url_for('listings.index'))
    if request.method == 'POST':
        listing = Listing(
            title=request.form['title'],
            type=request.form['type'],
            property_type=request.form['property_type'],
            price=float(request.form['price']),
            area_m2=int(request.form['area_m2']),
            rooms=int(request.form['rooms']),
            city=request.form['city'],
            address=request.form['address'],
            description=request.form['description'],
            user_id=current_user.id,
            agency_id=current_user.agency_id
        )
        db.session.add(listing)
        db.session.commit()
        flash('Annonce créée.', 'success')
        return redirect(url_for('listings.detail', id=listing.id))
    return render_template('new_listing.html')

@listings_bp.route('/listing/<int:id>/delete', methods=['POST'])
@login_required
def delete_listing(id):
    listing = Listing.query.get_or_404(id)
    if listing.user_id != current_user.id and current_user.role != 'admin':
        flash('Accès refusé.', 'danger')
        return redirect(url_for('listings.index'))
    db.session.delete(listing)
    db.session.commit()
    flash('Annonce supprimée.', 'success')
    return redirect(url_for('listings.index'))

@listings_bp.route('/listing/<int:id>/contact', methods=['POST'])
@login_required
def contact(id):
    c = Contact(user_id=current_user.id, listing_id=id, message=request.form['message'])
    db.session.add(c)
    db.session.commit()
    flash('Message envoyé à l\'agence.', 'success')
    return redirect(url_for('listings.detail', id=id))

@listings_bp.route('/listing/<int:id>/favorite', methods=['POST'])
@login_required
def toggle_favorite(id):
    fav = Favorite.query.filter_by(user_id=current_user.id, listing_id=id).first()
    if fav:
        db.session.delete(fav)
    else:
        db.session.add(Favorite(user_id=current_user.id, listing_id=id))
    db.session.commit()
    return redirect(url_for('listings.detail', id=id))
