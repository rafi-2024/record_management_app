from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, IntegerField
from wtforms.validators import DataRequired, Length


class IssueForm(FlaskForm):
    branch = StringField("Branch Reference",validators=[DataRequired(message="Branch Suffix ie /PA/DIG/SD required"), Length(min=5, max=20)])
    issue_date = DateField("Receipt Date",validators=[DataRequired(message="Issue Date must be supplied")])
    subject = StringField("Subject",validators=[DataRequired(message="Subject cannot be left Empty"), Length(min=5, max=60)]) 
    diary_id = StringField("Referance No")
    submit = SubmitField('Submit')

class ReminderForm(FlaskForm):
    diary_id = IntegerField("Reference ID",validators=[DataRequired(message="Reference ID is Required")])
    branch = StringField("Branch Reference",validators=[DataRequired(message="Branch Suffix ie /PA/DIG/SD required"), Length(min=5, max=20)])
    issue_date = DateField("Receipt Date",validators=[DataRequired(message="Issue Date must be supplied")])
    subject = StringField("Subject",validators=[DataRequired(message="Subject cannot be left Empty"), Length(min=5, max=60)]) 
    submit = SubmitField('Submit')

    