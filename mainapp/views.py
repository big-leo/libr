from mainapp import app, Session
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from mainapp.forms import LoginForm, SearchForm, NewBookForm, NewAuthorForm, EditBookForm, EditAuthorForm, AddAuthorForm
from mainapp.models import Book, Author, User
from sqlalchemy import or_

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    form.nickname.data = ''
    if request.method == 'POST' and form.validate():
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
    if request.method == 'POST' and form.validate():
        s.add(Book(name=form.name.data))
        s.commit()
        form.name.data = ''
    books = s.query(Book).all()
    return render_template('books.html', form=form, books=books)

@app.route('/book/<int:book_id>', methods=['GET', 'POST', 'DELETE'])
def book(book_id):
    form_n = EditBookForm()
    form_a = AddAuthorForm()
    s = Session()
    qb = s.query(Book)
    qa = s.query(Author)
    book = qb.get(book_id)
    if request.method == 'POST' and (form_n.validate() or form_a.validate()):
        if 'edit' in request.form:
            book.name = form_n.name.data
            s.commit()
        if 'add_author' in request.form:
            author = None
            try:
                author = qa.filter(Author.name==form_a.name.data)[0]
            except IndexError:
                print('Create new Author')
            if author:
                book.authors.append(author)
            else:
                book.authors.append(Author(name=form_a.name.data))
            s.commit()
        form_n.name.data = ''
        form_a.name.data = ''
    authors = [author for author in qa.filter(Author.books.any(Book.name==book.name))]
    return render_template('book.html', book=book, authors=authors, form_n=form_n, form_a=form_a)

@app.route('/del_book/<int:book_id>')
def del_book(book_id):
    s = Session()
    q = s.query(Book)
    book = q.get(book_id)
    if book:
        book.authors.clear()
        s.commit()
        s.delete(book)
        s.commit()
    return redirect('books')

@app.route('/del_book_author/<int:book_id>/<int:author_id>')
def del_book_author(book_id, author_id):
    s = Session()
    qb = s.query(Book)
    qa = s.query(Author)
    cur_book = qb.get(book_id)
    cur_author = qa.get(author_id)
    if book and author:
        cur_book.authors.remove(cur_author)
        s.commit()
    return book(book_id)

@app.route('/authors', methods=['GET', 'POST', 'DELETE'])
def authors():
    form = NewAuthorForm()
    s = Session()
    if request.method == 'POST' and form.validate():
        s.add(Author(name=form.name.data))
        s.commit()
        form.name.data = ''
    authors = s.query(Author).all()
    return render_template('authors.html', form=form, authors=authors)

@app.route('/author/<int:author_id>', methods=['GET', 'POST'])
def author(author_id):
    form_n = EditAuthorForm()
    form_a = AddAuthorForm()
    s = Session()
    qb = s.query(Book)
    qa = s.query(Author)
    author = qa.get(author_id)
    if request.method == 'POST' and (form_n.validate() or form_a.validate()):
        if 'edit' in request.form:
            author.name = form_n.name.data
            s.commit()
        if 'add_book' in request.form:
            book = None
            try:
                book = qb.filter(Book.name==form_a.name.data)[0]
            except IndexError:
                print('Create new Book')
            if book:
                author.books.append(book)
            else:
                author.books.append(Book(name=form_a.name.data))
            s.commit()
        form_n.name.data = ''
        form_a.name.data = ''
    books = [book for book in qb.filter(Book.authors.any(Author.name==author.name))]
    return render_template('author.html', author=author, books=books, form_n=form_n, form_a=form_a)

@app.route('/del_author/<int:author_id>')
def del_author(author_id):
    s = Session()
    q = s.query(Author)
    author = q.get(author_id)
    if author:
        author.books.clear()
        s.commit()
        s.delete(author)
        s.commit()
    return redirect('authors')

@app.route('/search', methods=['GET', 'POST'])
#@app.route('/search/<search_line>')
def search():
    form = SearchForm()
    books = []
    authors = []
    if request.method == 'POST' and form.validate():
        search_line = form.search.data
        if len(search_line) > 0:
            s = Session()
            books = [book for book in s.query(Book).all() if book.name.find(search_line) > -1]
            authors = [author for author in s.query(Author).all() if author.name.find(search_line) > -1]
    form.search.data = ''
    return render_template('search.html', title='Search', form=form, authors=authors, books=books)
