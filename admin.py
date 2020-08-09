from HMS import db, bcrypt
from HMS.models import User

username = 'admin'
password = 'admin'
email = 'admin@admin.admin'
hashPassword=bcrypt.generate_password_hash(password).decode('utf-8')

user = User(username=username, email=email, password=hashPassword)
db.session.add(user)
db.session.commit()

