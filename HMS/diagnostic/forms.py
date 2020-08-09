from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, IntegerField, StringField, DecimalField, HiddenField
from wtforms.validators import DataRequired, ValidationError
from HMS.models import DiagnosticMaster


class NonValidatingSelectField(SelectField):
    def pre_validate(self, form):
        pass


class DiagnosticSubmitForm(FlaskForm):
    submitId = HiddenField('', validators=[DataRequired()])
    #submitQty = HiddenField('', validators=[DataRequired()])
    update = SubmitField('Update')

class AddTestForm(FlaskForm):
    testName = StringField('Test Name', validators=[DataRequired()])
    rate = DecimalField('Rate', validators=[DataRequired()])
    submit = SubmitField('Add Test')

    def validate_testName(self, testName):
        test = DiagnosticMaster.query.filter_by(testName=testName.data).first()
        if test:
            raise ValidationError('This Test already exists')

class TestDeleteForm(FlaskForm):
    id = HiddenField(validators=[DataRequired()])
    submit = SubmitField('Confirm Delete')


class TestUpdateForm(FlaskForm):
    testName = StringField('Test Name', validators=[DataRequired()], render_kw={'readonly': True})
    rate = DecimalField('Rate', validators=[DataRequired()])
    submit = SubmitField('Update Test')
