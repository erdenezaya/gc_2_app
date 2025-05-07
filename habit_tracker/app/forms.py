from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField, SelectField
from wtforms.validators import DataRequired

class ShareHabitForm(FlaskForm):
    habit = SelectField('Choose a habit to share:', coerce=int, validators=[DataRequired()])
    recipient = StringField('Share with (username):', validators=[DataRequired()])
    submit = SubmitField('Share')