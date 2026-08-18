from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class StaffTrekForm(FlaskForm):
    available_slots = IntegerField("Available Slots",validators=[ DataRequired(),NumberRange(min=0, max=300) ])
    status = SelectField("Status",
                          choices=[
                                   ("Open", "Open"),
                                   ("Closed", "Closed")] )

    submit = SubmitField("Update Trek")