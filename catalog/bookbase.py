from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_build import Base, BookShelf, Book

engine = create_engine('sqlite:///minilibrary.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()


bookshelf1 = BookShelf(id = 1, category = "Compueter Programming")
session.add(bookshelf1)
session.commit()

book1 = Book(bookshelf_id = 1, id = 1, name = "Algorithms",
             descreption = "This is the book that mainly describes algorithm.",
             price = 10.34)
session.add(book1)
session.commit()


book2 = Book(bookshelf_id = 1, id = 2, name = "Database",
             descreption = "This is the book that describes the database.",
             price = 13.33)
session.add(book2)
session.commit()

book3 = Book(bookshelf_id = 1, id = 3, name = "Operating System",
             descreption = "This is the book that describes the operating system",
             price = 15.22)
session.add(book3)
session.commit()

bookshelf2 = BookShelf(id = 2, category = "Cooking books")
session.add(bookshelf2)
session.commit()

book4 = Book(bookshelf_id = 2, id = 4, name = "How to make Chinese noodles",
             descreption = "This is the book that teach you how to make Chinese \
                            noodles", price = 24.35)
session.add(book4)
session.commit()

book5 = Book(bookshelf_id = 2, id = 5, name = "French dish basics",
             descreption = "This is the book that tells the basic skills when \
                            preparing french dishes", price = 21.13)
session.add(book5)
session.commit()

book6 = Book(bookshelf_id = 2, id = 6, name = "Impressive sushi",
             descreption = "This is the book that shows some fantastic sushi \
                            prepared by famous chefs", price = 36.08)
session.add(book6)
session.commit()

book7 = Book(bookshelf_id = 2, id = 7, name = "Food and cooking",
             descreption = "This book has a brief introduction about the properties \
                           of some common food and how to cook them", price = 67.32)
session.add(book7)
session.commit()

bookshelf3 = BookShelf(id = 3, category = "phycology books")
session.add(bookshelf3)
session.commit()

book8 = Book(bookshelf_id = 3, id = 8, name = "WillPower",
             descreption = "This book has a brief introduction about the beniefits \
                            willpower and how to reinforce it", price = 7.54)
session.add(book8)
session.commit()

book9 = Book(bookshelf_id = 3, id = 9, name = "asperger syndrome",
             descreption = "This book has makes a brief introduction about the \
                            asperger syndrome", price = 15.34)
session.add(book9)
session.commit()

print "all books inserted!"

