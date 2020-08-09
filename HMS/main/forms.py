from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, regexp, ValidationError
from HMS.models import Patient


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class SearchForm(FlaskForm):
    patientid = StringField('Patient ID', validators=[DataRequired(), regexp('\d{9}$', message='Patient Id must have 9 digits')], render_kw={"placeholder":"Patient Id"})
    submit = SubmitField('Search')
    
    def validate_patientid(self, patientid):
        if Patient.query.filter_by(patientId=self.patientid.data).first() is None:
            raise ValidationError('Patient with given Id not Exists')