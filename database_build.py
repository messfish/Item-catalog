import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

engine = create_engine('sqlite:///minilibrary.db')
Base.metadata.create_all(engine)
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

class BookShelf(Base):
    __tablename__ = 'bookshelf'

    id = Column(Integer, primary_key = True)
    category = Column(String(50), nullable = False)

    @property
    def convertToJSON(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'books': [
                book.convertoJSON for book in getBookList(self.id)
            ],
        }

    def getBookList(id):
        return session.query(Book).filter_by(id = id)

class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key = True)
    bookshelf_id = Column(Integer, ForeignKey('bookshelf.id'), primary_key = True)
    name = Column(String(50), nullable = False)
    descreption = Column(Text(500))
    price = Column(Float, default = 0.0)
    bookshelf = relationship(BookShelf)

    @property
    def convertToJSON(self):
        return {
            'name' : self.name,
            'descreption' : self.id,
            'price' : self.price,
            'id' : self.id,
        }

    
    

    
