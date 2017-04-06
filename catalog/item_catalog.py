from flask import Flask, render_template, request, url_for, redirect, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_build import Base, BookShelf, Book

engine = create_engine("sqlite:///minilibrary.db")
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

# By default, this method is used to get a list of bookshelves.
@app.route('/')
def BookShelfCatalog():
    bookshelves = session.query(BookShelf).all()
    return render_template('catalog.html', bookshelves = bookshelves)

# this method is used to get a single book shelf by using the id
# and get a list of books on that book shelf.
@app.route('/bookshelf/<int:bookshelf_id>/')
def Bookshelf(bookshelf_id):
    bookshelf = session.query(BookShelf).filter_by(id = bookshelf_id).one()
    books = session.query(Book).filter_by(bookshelf_id = bookshelf_id)
    return render_template('books.html', bookshelf = bookshelf, books = books)

# this method is used to create a new bookshelf and store it in the database.
@app.route('/bookshelf/new/', methods=['POST','GET'])
def newBookShelf():
    if request.method == 'POST':
        newBookShelf = BookShelf(category = request.form['name'])
        session.add(newBookShelf)
        session.commit()
        flash("we get a new book shelf!")
        return redirect(url_for('BookShelfCatalog'))
    else:
        return render_template('newbookshelf.html')

# this method is used to create a new book and store it in the database.    
@app.route('/bookshelf/<int:bookshelf_id>/new/', methods=['POST','GET'])
def newBook(bookshelf_id):
    if request.method == 'POST':
        getPrice = request.form['price']
        if request.form['price'] == "":
            getPrice = 0.0
        newBook = Book(bookshelf_id = bookshelf_id,
                       name = request.form['name'],
                       descreption = request.form['descreption'],
                       price = float(getPrice))
        session.add(newBook)
        session.commit()
        flash("we get a new book!")
        return redirect(url_for('Bookshelf', bookshelf_id = bookshelf_id))
    else:
        return render_template('newbook.html', bookshelf_id = bookshelf_id)

# this method is used for editing an existing book.
@app.route('/bookshelf/<int:bookshelf_id>/<int:book_id>/edit', methods=['POST','GET'])
def editBook(bookshelf_id, book_id):
    editedBook = session.query(Book).filter_by(bookshelf_id = bookshelf_id,
                    id = book_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedBook.name = request.form['name']
        if request.form['descreption']:
            editedBook.description = request.form['descreption']
        if request.form['price']:
            editedBook.price = request.form['price']
        session.add(editedBook)
        session.commit()
        flash("One book is modified!")
        return redirect(url_for('Bookshelf', bookshelf_id = bookshelf_id))
    else:
        return render_template('editbook.html', bookshelf_id = bookshelf_id,
                               book_id = book_id, book = editedBook)

# this method is used for deleting an existing book.
@app.route('/bookshelf/<int:bookshelf_id>/<int:book_id>/delete', methods=['POST','GET'])
def deleteBook(bookshelf_id, book_id):
    deletedBook = session.query(Book).filter_by(bookshelf_id = bookshelf_id,
                     id = book_id).one()
    if request.method == 'POST':
        session.delete(deletedBook)
        session.commit()
        flash("One book is deleted!")
        return redirect(url_for('Bookshelf', bookshelf_id = bookshelf_id))
    else:
        return render_template('deletebook.html', bookshelf_id = bookshelf_id,
                                book_id = book_id, book = deletedBook)

# this is used to make an API Endpint for all the elements(GET Request)
@app.route('/bookshelf/JSON/')
def wholeJSON():
    bookshelves = session.query(BookShelf)
    return jsonify(Library = [bookshelf.convertToJSON
                                  for bookshelf in bookshelves])

# this is used to make an API Endpoint for all books in a bookshelf(GET Request)
@app.route('/bookshelf/<int:bookshelf_id>/books/JSON/')
def booksJSON(bookshelf_id):
    books = session.query(Book).filter_by(bookshelf_id = bookshelf_id)
    return jsonify(Books = [book.convertToJSON for book in books])

# this is used to make an API Endpoint for a single book(GET Request)
@app.route('/bookshelf/<int:bookshelf_id>/<int:book_id>/book/JSON')
def bookJSON(bookshelf_id, book_id):
    book = session.query(Book).filter_by(bookshelf_id = bookshelf_id,
                                        id = book_id).one()
    return jsonify(Book = book.convertToJSON)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
