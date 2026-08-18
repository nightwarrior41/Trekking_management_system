from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,SelectField,IntegerField,DateField
from wtforms.validators import DataRequired,Length,ValidationError,NumberRange
from app.models import User,Trek

class TrekForm(FlaskForm):       
    trek_name = StringField("Trek Name",validators = [DataRequired(),Length(min=2,max=100)])
    location = StringField("Location",validators = [DataRequired(),Length(min=2,max=100)])
    difficulty = SelectField("Difficulty", choices=[
        ("Easy","Easy"),
        ("Moderate","Moderate"),
        ("Hard","Hard")],validators = [DataRequired()])
    
    duration = IntegerField("Duration",validators = [DataRequired(),NumberRange(min=1,max=30)])
    available_slots = IntegerField("Available Slots",validators = [DataRequired(),NumberRange(min=1,max=300)])
    start_date = DateField("Start Date",validators=[DataRequired()])
    end_date = DateField("End Date",validators=[DataRequired()])
    status = SelectField("Status",    choices=[
        ("Upcoming","Upcoming"),
        ("Open","Open"),
        ("Completed","Completed"),
        ("Cancelled","Cancelled")
    ],validators=[DataRequired()])
    
    assigned_staff = SelectField("Assign Staff",coerce=int)
    submit = SubmitField("Create Trek")
    
    def validate_end_date(self, end_date):
        if end_date.data < self.start_date.data:
            raise ValidationError("End date must be after the start date.")