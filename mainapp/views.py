from mainapp import app, Session
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from mainapp.forms import LoginForm, SearchForm, NewBookForm, NewAuthorForm, AddAuthorForm
from mainapp.models import Book, Author, User
from sqlalchemy import or_

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        user = Session().query(User).filter_by(nickname=form.nickname.data).first()
        if user == None:
            flash('Login requested for nickname=' + form.nickname.data)
        else:
            flash('Logined with nickname=' + form.nickname.data)
            g.user = user
        return redirect('/')
    return render_template('login.html', title='Sign in', form=form)

@app.route('/user/<nickname>')
#@login_required
def user(nickname):
    user = Session().query(User).filter_by(nickname=nickname).first()
    if user == None:
        flash('User' + nickname + ' not found.')
        return redirect(url_for('index'))
    return render_template('user.html', user=user)

@app.route('/user')
def cur_user():
    try:
        if g.user:
            return render_template('user.html', user=g.user)
    except AttributeError:
        flash('Please login with nickname "admin".')
        return redirect(url_for('index'))

@app.route('/')
def index():
    books = Session().query(Book).all()
    return render_template('index.html', books=books)

@app.route('/books', methods=['GET', 'POST', 'DELETE'])
def books():
    form = NewBookForm()
    s = Session()
    q = s.query(Book)
    if request.method == 'POST':
        s.add(Book(name=form.name.data))
        s.commit()
    if request.method == 'DELETE':
        s.delete(q.filter(Book.name==form.name.data))
        s.commit()
    books = s.query(Book).all()
    return render_template('books.html', form=form, books=books)

@app.route('/authors', methods=['GET', 'POST', 'DELETE'])
def authors():
    form = NewAuthorForm()
    s = Session()
    if request.method == 'POST':
        s.add(Author(name=form.name.data))
        s.commit()
    authors = s.query(Author).all()
    return render_template('authors.html', form=form, authors=authors)

@app.route('/book/<int:book_id>')
def book(book_id):
    s = Session()
    book = s.query(Book).get(book_id)
    authors = [author for author in s.query(Author).filter(Author.books.any(Book.name==book.name))]
    return render_template('book.html', book=book, book_id=book_id, authors=authors)

@app.route('/author/<int:author_id>')
def author(author_id):
    s = Session()
    author = s.query(Author).get(author_id)
    books = [book for book in s.query(Book).filter(Book.authors.any(Author.name==author.name))]
    return render_template('author.html', author=author, books=books, author_id=author_id)

@app.route('/search', methods=['GET', 'POST'])
#@app.route('/search/<search_line>')
def search():
    form = SearchForm()
    books = []
    authors = []
    if request.method == 'POST':
        search_line = form.search.data
        if len(search_line) > 0:
            s = Session()
            books = [book for book in s.query(Book).all() if book.name.startswith(search_line) or (book.name.find(search_line) > 0)]
            authors = [author for author in s.query(Author).all() if author.name.startswith(search_line) or (author.name.find(search_line) > 0)]
    return render_template('search.html', title='Search', form=form, authors=authors, books=books)
