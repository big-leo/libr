from flask.ext.wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import Required, InputRequired

class LoginForm(Form):
    nickname = TextField('nickname', validators = [Required()])
    #remember_me = BooleanField('remember_me', default=False)

class SearchForm(Form):
    search = TextField('search', validators = [Required()])

class NewBookForm(Form):
    name = TextField('name', validators = [Required()])

class NewAuthorForm(Form):
    name = TextField('name', validators = [Required()])

class EditBookForm(Form):
    #old_name = TextField('Old name', validators = [Required()])
    name = TextField('name', validators = [Required()])

class EditAuthorForm(Form):
    #old_name = TextField('Old name', validators = [Required()])
    name = TextField('name', validators = [Required()])

class AddAuthorForm(Form):
    #book_name = TextField('Book name', validators = [Required()])
    name = TextField('name', validators = [Required()])
