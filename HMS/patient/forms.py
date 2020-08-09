from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, DateTimeField, HiddenField, IntegerField
from wtforms.validators import DataRequired, regexp, ValidationError, optional
from HMS.cities import getstates, getcities
from HMS.models import Patient
from datetime import datetime


class NonValidatingSelectField(SelectField):
    def pre_validate(self, form):
        pass


class PatientRegistrationForm(FlaskForm):
    ssnid = StringField('Patient SSN Id', validators=[DataRequired()], render_kw={'readonly': True})
    patientName = StringField('Patient Name', validators=[DataRequired()])
    age = IntegerField('Patient Age', validators=[DataRequired()])
    dateOfAdmission = DateTimeField('Date of Admission', validators=[DataRequired()], default=datetime.now().replace(microsecond=0), render_kw={'readonly': True})
    roomType = SelectField('Type of Bed', validators=[DataRequired()], choices=[('', 'Select Room'),('General', 'General ward'),('Sharing', 'Semi sharing'), ('Single', 'Single room')])
    patientaddress = TextAreaField('Address', validators=[DataRequired()])
    state = SelectField('State', validators=[DataRequired()], choices=[(state,state) for state in getstates()])
    city = NonValidatingSelectField('City', validators=[DataRequired()], choices=[])
    submit = SubmitField('Submit')

    def validate_dateOfAdmission(self, dateOfAdmission):
        if self.dateOfAdmission.data > datetime.now():
            raise ValidationError('Please provide correct date of admission')

    def validate_age(self, age):
        if int(self.age.data) > 150:
            raise ValidationError('Age must be below 150')


class PatientUpdateForm(FlaskForm):
    patientId = StringField('Patient Id', validators=[DataRequired()], render_kw={'readonly': True})
    name = StringField('Patient New Name', validators=[optional()])
    age = StringField('Patient New Age', validators=[optional()])
    address = TextAreaField('New Address', validators=[optional()])
    state = SelectField('State', validators=[optional()], choices=[(state,state) for state in getstates()])
    city = NonValidatingSelectField('City', validators=[optional()], choices=[])
    submit = SubmitField('Update')


class PatientDelete(FlaskForm):
    pid = HiddenField(validators=[DataRequired()])
    submit = SubmitField('Confirm Delete')


class PatientDischarge(FlaskForm):
    pid = HiddenField(validators=[DataRequired()])
    nexturl = HiddenField(validators=[DataRequired()])
    dateOfDischarge = HiddenField(validators=[DataRequired()], default=datetime.now().replace(microsecond=0))
    formData = HiddenField(validators=[DataRequired()])
    submit = SubmitField('Confirm & Proceed')
