from wtforms import Form, StringField, TextAreaField, PasswordField, validators

# Register Form Class
class RegisterForm(Form):
    fname = StringField('FirstName', [validators.Length(min=1, max=50)])
    lname = StringField('Lastname', [validators.Length(min=1, max=25)])
    cnumber = StringField('PhoneNumber', [validators.Length(min=3, max=50)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    address = StringField('Complete Address', [validators.Length(min=5, max=100)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
        ])
    confirm = PasswordField('Confirm Password')
