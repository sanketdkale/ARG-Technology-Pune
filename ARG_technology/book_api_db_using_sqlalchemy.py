from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_basicauth import BasicAuth

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'admin'
basic_auth = BasicAuth(app)

DATABASE_URL = "postgresql://username:password@localhost/database_name"
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    author = db.Column(db.String)
    isbn = db.Column(db.String, unique=True)
    description = db.Column(db.String)
    price = db.Column(db.Integer)

    def __init__(self, title, author, isbn, description, price):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.description = description
        self.price = price


@app.route('/books', methods=['POST'])
@basic_auth.required
def add_book():
    data = request.get_json()
    new_book = Book(
        title=data['title'],
        author=data['author'],
        isbn=data['isbn'],
        description=data['description'],
        price=data['price']
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book added successfully'})


@app.route('/books/<isbn>', methods=['GET'])
@basic_auth.required
def get_book(isbn):
    book = Book.query.filter_by(isbn=isbn).first()
    if book:
        return jsonify({
            'title': book.title,
            'author': book.author,
            'isbn': book.isbn,
            'description': book.description,
            'price': book.price
        })
    else:
        return jsonify({'message': 'Book not found'}), 404


@app.route('/books/<isbn>', methods=['PUT'])
@basic_auth.required
def update_book(isbn):
    data = request.get_json()
    book = Book.query.filter_by(isbn=isbn).first()
    if book:
        if 'title' in data:
            book.title = data['title']
        if 'author' in data:
            book.author = data['author']
        if 'description' in data:
            book.description = data['description']
        if 'price' in data:
            book.price = data['price']
        db.session.commit()
        return jsonify({'message': 'Book updated successfully'})
    else:
        return jsonify({'message': 'Book not found'}), 404


@app.route('/books/<isbn>', methods=['DELETE'])
@basic_auth.required
def delete_book(isbn):
    book = Book.query.filter_by(isbn=isbn).first()
    if book:
        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': 'Book deleted successfully'})
    else:
        return jsonify({'message': 'Book not found'}), 404


@app.route('/books', methods=['GET'])
@basic_auth.required
def list_books():
    books = Book.query.all()
    book_list = []
    for book in books:
        book_list.append({
            'title': book.title,
            'author': book.author,
            'isbn': book.isbn
        })
    return jsonify(book_list)


if __name__ == '__main__':
    app.run(debug=True)
