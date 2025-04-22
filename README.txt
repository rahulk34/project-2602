# Apartment Project (Clean Setup)

## ✅ How to Run

1. Navigate to the folder:
   cd path/to/apartment_project

2. Create and activate virtual environment:
   python -m venv venv
   venv\Scripts\activate

3. Install dependencies:
   pip install -r requirements.txt

4. Create DB and add users:
   python
   >>>
   from app import app, db
   from app.models.user import User
   with app.app_context():
       db.create_all()
       db.session.add(User(username='bob', password='bobpass', role='landlord'))
       db.session.add(User(username='alice', password='alicepass', role='tenant'))
       db.session.commit()
   exit()

5. Run the app:
   python run.py
