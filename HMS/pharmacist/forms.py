from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, IntegerField, StringField, DecimalField, HiddenField
from wtforms.validators import DataRequired, ValidationError
from HMS.models import MedicineMaster


class MedicineSubmitForm(FlaskForm):
    submitId = HiddenField('', validators=[DataRequired()])
    submitQty = HiddenField('', validators=[DataRequired()])
    update = SubmitField('Update')

class MedicineStoreForm(FlaskForm):
    medicineName = StringField('Medicine Name', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    rate = DecimalField('Rate', validators=[DataRequired()])
    submit = SubmitField('Add Medicine')

    def validate_medicineName(self, medicineName):
        if MedicineMaster.query.filter_by(medicineName=medicineName.data).first():
            raise ValidationError('This Medicine is already exists')


class MedicineDeleteForm(FlaskForm):
    id = HiddenField(validators=[DataRequired()])
    submit = SubmitField('Confirm Delete')


class MedicineUpdateForm(FlaskForm):
    medicineName = StringField('Medicine Name', validators=[DataRequired()], render_kw={'readonly': True})
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    rate = DecimalField('Rate', validators=[DataRequired()])
    submit = SubmitField('Update Medicine')
