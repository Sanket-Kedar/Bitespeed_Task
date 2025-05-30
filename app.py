import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, Contact
from sqlalchemy import or_
from dotenv import load_dotenv

# load from .env for local development
load_dotenv()  

# initialize Flask app and SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")  # PostgreSQL URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# endpoint to check if the API is running 
@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "API is up and running!"}), 200

# endpoint to identify or create a contact based on email or phone number
@app.route('/identify', methods=['POST'])
def identify():
    data = request.json
    email = data.get("email")
    phone = data.get("phoneNumber")

    if not email and not phone:
        return jsonify({"error": "Either email or phoneNumber must be provided"}), 400

    matched_contacts = Contact.query.filter(
        or_(
            Contact.email == email,
            Contact.phoneNumber == phone
        )
    ).order_by(Contact.createdAt).all()

    if not matched_contacts:
        new_contact = Contact(email=email, phoneNumber=phone)
        db.session.add(new_contact)
        db.session.commit()
        return jsonify({
            "contact": {
                "primaryContactId": new_contact.id,
                "emails": [new_contact.email] if new_contact.email else [],
                "phoneNumbers": [new_contact.phoneNumber] if new_contact.phoneNumber else [],
                "secondaryContactIds": []
            }
        })

    primary_contact = None
    secondary_ids = []

    for contact in matched_contacts:
        if contact.linkPrecedence == "primary":
            if primary_contact is None or contact.createdAt < primary_contact.createdAt:
                primary_contact = contact

    for contact in matched_contacts:
        if contact.id != primary_contact.id:
            contact.linkPrecedence = "secondary"
            contact.linkedId = primary_contact.id
            secondary_ids.append(contact.id)

    db.session.commit()

    existing_emails = set(c.email for c in matched_contacts if c.email)
    existing_phones = set(c.phoneNumber for c in matched_contacts if c.phoneNumber)

    new_contact_created = False
    if (email and email not in existing_emails) or (phone and phone not in existing_phones):
        new_contact = Contact(
            email=email,
            phoneNumber=phone,
            linkedId=primary_contact.id,
            linkPrecedence='secondary'
        )
        db.session.add(new_contact)
        db.session.commit()
        secondary_ids.append(new_contact.id)
        new_contact_created = True

    final_contacts = Contact.query.filter(
        (Contact.id == primary_contact.id) | (Contact.linkedId == primary_contact.id)
    ).all()

    all_emails = list({c.email for c in final_contacts if c.email})
    all_phones = list({c.phoneNumber for c in final_contacts if c.phoneNumber})
    all_secondary_ids = [c.id for c in final_contacts if c.linkPrecedence == 'secondary']

    return jsonify({
        "contact": {
            "primaryContactId": primary_contact.id,
            "emails": all_emails,
            "phoneNumbers": all_phones,
            "secondaryContactIds": all_secondary_ids
        }
    })

if __name__ == '__main__':
    app.run(debug=True)
