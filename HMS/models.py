from HMS import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'userstore'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f'username : {self.username}, email : {self.email}' 


class Patient(db.Model):
    __tablename__ = 'patient'
    ssnid = db.Column(db.String(9), primary_key=True)
    patientId = db.Column(db.String(9), nullable=False, unique=True)
    name = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    dateOfJoining = db.Column(db.DateTime, nullable=False)
    dateOfDischarge = db.Column(db.DateTime)
    roomType = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    state = db.Column(db.String(30), nullable=False)
    status = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return f'ssnid : {self.ssnid}, patientName : {self.name}'

class MedicineMaster(db.Model):
    __tablename__ = 'medicinemaster'
    medicineId = db.Column(db.Integer, primary_key=True)
    medicineName = db.Column(db.String(100), nullable=False, unique=True)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    rate = db.Column(db.Float, nullable=False, default=0)

    def __repr__(self):
        return f'medicineId : {self.medicineId}, medicineName : {self.medicineName}, quantity : {self.quantity}, rate : {self.rate}'

class DiagnosticMaster(db.Model):
    __tablename__ = 'diagnosticmaster'
    testId = db.Column(db.Integer, primary_key=True)
    testName = db.Column(db.String(100), nullable=False, unique=True)
    rate = db.Column(db.Float, nullable=False, default=0)

    def __repr__(self):
        return f'testId : {self.testId}, testName : {self.testName}, rate : {self.rate}'

class Medicines(db.Model):
    __tablename__ = 'medicines'
    id = db.Column(db.Integer, primary_key=True)
    patientId = db.Column(db.String(9), db.ForeignKey('patient.patientId'), nullable=False)
    medicineId = db.Column(db.Integer, db.ForeignKey('medicinemaster.medicineId'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'patientId : {self.patientId}, medicineId : {self.medicineId}'


class Diagnostics(db.Model):
    __tablename__ = 'diagnostics'
    id = db.Column(db.Integer, primary_key=True)
    patientId = db.Column(db.String(9), db.ForeignKey('patient.patientId'), nullable=False)
    testId = db.Column(db.Integer, db.ForeignKey('diagnosticmaster.testId'), nullable=False)

    def __repr__(self):
        return f'patientId : {self.patientId}, testId : {self.testId}'
