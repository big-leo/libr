from flask.ext.wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import Required

class LoginForm(Form):
    nickname = TextField('nickname', validators = [Required()])
    #remember_me = BooleanField('remember_me', default=False)

class SearchForm(Form):
    search = TextField('Search', validators = [Required()])

class NewBookForm(Form):
    name = TextField('Name', validators = [Required()])

class NewAuthorForm(Form):
    name = TextField('Name', validators = [Required()])

class AddAuthorForm(Form):
    book_name = TextField('Book name', validators = [Required()])
    author_name = TextField('Author name', validators = [Required()])
