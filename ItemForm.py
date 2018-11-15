from wtforms import Form, StringField, TextAreaField, PasswordField, validators


# Item Form Class
class ItemForm(Form):
    itemname = StringField('Itemname', [validators.Length(min=1, max=200)])
    description = TextAreaField('Description', [validators.Length(min=30)])
    price = StringField('Price(php)', [validators.Length(min=1, max=200)])
    category = StringField('Category', [validators.Length(min=1, max=200)])
    photo = StringField('Photo', [validators.Length(min=1, max=200)])
    unitsno = StringField('Available Unit', [validators.Length(min=1, max=200)])