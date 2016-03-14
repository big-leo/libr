from mainapp import app, Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref

association_table = Table('association', Base.metadata,
    Column('book_id', Integer, ForeignKey('book.id')),
    Column('author_id', Integer, ForeignKey('author.id'))
)

class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    name =  Column(String(50))
#    book_id = Column(Integer, ForeignKey('book.id'))
    books = relationship("Book", secondary=association_table, backref="author")

    def __repl__(self):
        return self.name

class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    name =  Column(String(50))
    authors = relationship("Author", secondary=association_table, backref="book")

    def __repl__(self):
        return self.name

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    nickname =  Column(String(50))

    def __repl__(self):
        return self.nickname
