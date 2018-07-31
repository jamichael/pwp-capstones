import random

class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        print("Current email {cEmail} is now {nEmail}".format(cEmail = self.email, nEmail = address))
        self.email = address

    def __repr__(self):
        return "User: {user}\nEmail: {email}\nBooks Read: {books}".format(user = self.name, email = self.get_email(), books = len(self.books))

    def __eq__(self, other_user):
        #Do error checking here later
        return self.name == other_user

    def read_book(self, book, rating = None):
        self.books[book] = rating

    def get_average_rating(self):
        average = 0
        for index in self.books.values():
            if not index == None:
              average += index

        return average / len(self.books)

class Book(object):
    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.ratings = []
        self.lowest_rating = 0
        self.highest_rating = 4

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, new_ISBN):
        print("Current ISBN {oISBN} is now {nISBN}".format(oISBN = self.get_isbn(), nISBN = new_ISBN ) )
        self.isbn = new_ISBN

    def add_rating(self, rating):
        if type(rating) == int:
          if rating >= self.lowest_rating and rating <= self.highest_rating:
            self.ratings.append(rating)
          else:
            print("{rate} is an invalid rating. Please keep it between {lRating} and {hRating}".format(rate = rating, lRating = self.lowest_rating, hRating = self.highest_rating) )
        else:
            print("Invalid Rating")

    def __eq__(self, other_book):
        #Do error checking here later
        if other_book != None:
          return self.title == other_book.title and self.get_isbn() == other_book.get_isbn()
        else:
          return False

    def get_average_rating(self):
        average = 0
        for index in self.ratings:
            average += index

        return average / len(self.ratings)

    def __hash__(self):
        return hash( (self.title, self.isbn) )

  
class Fiction(Book):
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return "{title} by {author}".format(title = self.get_title(), author = self.get_author())

class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return  "{title}, a {level} manual on {subject}".format(title = self.get_title(), level = self.get_level(), subject = self.get_subject())

class TomeRater(object):
    def __init__(self):
        self.users = {}
        self.books = {}

    def create_book(self, title, isbn):
        return Book(title, self.unique_isbn)

    def create_novel(self, title, author, isbn):
        return Fiction(title, author, isbn)

    def create_non_fiction(self, title, subject, level, isbn):
        return Non_Fiction(title, subject, level, isbn)

    def add_book_to_user(self, book, email, rating = None):
        if self.users.get(email) != None:

          #ISBN unique check... I dont think it's efficient to call it here
          if(self.books.get(book) == None ):
            book.set_isbn( self.unique_isbn(book.get_isbn()) )
            
          self.users[email].read_book(book, rating)
            
          book.add_rating(rating)

          if self.books.get(book) == None:
              self.books[book] = 1
          else:
              self.books[book] +=1
        else:
            print("No user with email {pemail}".format(pemail = email) )

    def add_user(self, name, email, user_books = None):
        if self.users.get(email) == None:
           if self.valid_email_format(email) == True:
            self.users[email] = User(name, email)
            if user_books is not None:
              for index in user_books:
                self.add_book_to_user(index, email )
        else:
            print("{user} already exists!".format(user = name))



    def print_catalog(self):
        for book in self.books.keys():
            print(book)

    def print_users(self):
        for email in self.users.values():
            print(email)

    def get_most_read_book(self):
        currentBook = None

        for book,readings in self.books.items():
            if currentBook == None:
                currentBook = book
            else:
                if self.books[currentBook] < readings:
                    currentBook = book
        return currentBook


    def highest_rated_book(self):
        currentBook = None

        for book in self.books.keys():
            if currentBook == None:
                currentBook = book
            elif currentBook != book and currentBook.get_average_rating() < book.get_average_rating():
                currentBook = book
        return currentBook

    def most_positive_user(self):
        currentUser = None

        for email,user in self.users.items():
            if currentUser == None:
                currentUser = user
            else:
                if self.users[currentUser.get_email()].get_average_rating() < self.users[email].get_average_rating():
                    currentBook = user
        return currentUser

    def unique_isbn(self, isbn):
        for index in self.books.keys():
            if index.get_isbn() == isbn:
                print("ISBN {pISBN} is already in use! Generating a custom ISBN now.".format(pISBN = isbn) )
                return random.randrange(1000000000000, 9999999999999, 10)
        return isbn

    def valid_email_format(self, email):
        if type(email) == str:
            if email.find('@') != -1: 
                if email.find('.com') != -1 or email.find('.edu') != -1 or email.find('.org') != -1:
                    print("{pemail} is a valid email address".format(pemail = email) )
                    return True

        print("{pemail} is not a valid email address".format(pemail = email) )
        return False




