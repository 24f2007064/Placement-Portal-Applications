from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class RegestrationForm(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    email = StringField("Email", validators=[DataRequired(message="what you think?? are we gonna send you NUdes!?, then why dont you put your mail here?"), Email(message="MF its not a eMail..")])
    submit = SubmitField("Regester")