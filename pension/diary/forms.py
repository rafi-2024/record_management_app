from datetime import date
from flask import abort
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DateField, FormField, FileField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Optional
from pension.models import Diary

def validate_date(form, field):
    if field.data > date.today():
        raise ValidationError(f"The date you entered {field.data} cannot be in the Future! Today date is {date.today()}")



class ReferanceForm(FlaskForm):
    reference = StringField("Referance No",validators=[DataRequired(), Length(min=5, max=25)])
    ref_date = DateField("Receipt Date",validators=[DataRequired(), validate_date])

class AddRefs(FlaskForm):
    ref_id = IntegerField("Reference ID",validators=[DataRequired(message="Reference ID is Required")])
    subject = StringField("Subject",validators=[DataRequired(message="Subject is required"), Length(min=5, max=60)]) 
    reference = StringField("Referance No",validators=[DataRequired(message="Reference Number is required"), Length(min=5, max=25)])
    ref_date = DateField("Receipt Date",validators=[DataRequired(message="Reference Date is required"), validate_date])
    submit = SubmitField('Submit')
    


class DiaryForm(FlaskForm):
    reference = StringField("Referance No",validators=[DataRequired(), Length(min=5, max=25)])
    ref_date = DateField("Receipt Date",validators=[DataRequired(), validate_date] )
    subject = StringField("Subject",validators=[DataRequired(), Length(min=5, max=60)])
    diary_id = IntegerField("Diary No", validators=[Optional(strip_whitespace=True)])
    submit = SubmitField('Submit')

class UploadForm(FlaskForm):
    file = FileField()
    submit = SubmitField('UPLOAD')
