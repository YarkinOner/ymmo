from app import create_app, bcrypt
from models import db, User, Agency, Listing

app = create_app()

with app.app_context():
    agency = Agency(name="Ymmo Siège", city="Aix-en-Provence", address="1 rue de la Paix")
    db.session.add(agency)
    db.session.flush()

    admin = User(
        name="Admin",
        email="admin@ymmo.fr",
        password_hash=bcrypt.generate_password_hash("admin123").decode('utf-8'),
        role="admin",
        agency_id=agency.id
    )
    db.session.add(admin)
    db.session.flush()

    listings = [
        Listing(title="Appartement moderne 3 pièces", type="vente", property_type="appartement",
                price=250000, area_m2=75, rooms=3, city="Marseille",
                address="12 rue Saint-Ferréol", description="Bel appartement rénové en centre-ville.",
                user_id=admin.id, agency_id=agency.id),
        Listing(title="Maison avec jardin", type="vente", property_type="maison",
                price=420000, area_m2=140, rooms=5, city="Aix-en-Provence",
                address="5 avenue des Platanes", description="Grande maison familiale avec jardin de 500m².",
                user_id=admin.id, agency_id=agency.id),
        Listing(title="Studio centre-ville", type="location", property_type="appartement",
                price=650, area_m2=28, rooms=1, city="Lyon",
                address="8 rue de la République", description="Studio lumineux, idéal étudiant.",
                user_id=admin.id, agency_id=agency.id),
    ]
    for l in listings:
        db.session.add(l)

    db.session.commit()
    print("Base de données initialisée !")