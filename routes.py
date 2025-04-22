from flask import render_template, request, redirect, url_for, session
from functools import wraps
from app import app, db
from app.models.user import User
from app.models.apartment import Apartment
from app.models.review import Review

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = session.get('token')
        if not token or token != 'bobpass':
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def home():
    location = request.args.get('location')
    amenities = request.args.get('amenities')
    query = Apartment.query
    if location:
        query = query.filter(Apartment.location.contains(location))
    if amenities:
        query = query.filter(Apartment.amenities.contains(amenities))
    apartments = query.all()
    return render_template('home.html', apartments=apartments)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['token'] = 'bobpass'
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/create_apartment', methods=['GET', 'POST'])
@token_required
def create_apartment():
    if request.method == 'POST':
        title = request.form['title']
        location = request.form['location']
        amenities = request.form['amenities']
        description = request.form['description']
        new_apartment = Apartment(title=title, location=location, amenities=amenities, description=description, landlord_id=1)
        db.session.add(new_apartment)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_apartment.html')

@app.route('/apartment/<int:id>', methods=['GET', 'POST'])
def apartment_detail(id):
    apartment = Apartment.query.get_or_404(id)
    reviews = Review.query.filter_by(apartment_id=id).all()
    if request.method == 'POST':
        content = request.form['content']
        rating = int(request.form['rating'])
        new_review = Review(content=content, rating=rating, apartment_id=id, tenant_id=2)
        db.session.add(new_review)
        db.session.commit()
        return redirect(url_for('apartment_detail', id=id))
    return render_template('reviews.html', apartment=apartment, reviews=reviews)
