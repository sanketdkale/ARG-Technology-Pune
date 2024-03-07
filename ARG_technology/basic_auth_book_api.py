from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'user1'
app.config['BASIC_AUTH_PASSWORD'] = 'password1'
app.config['BASIC_AUTH_FORCE'] = True
basic_auth = BasicAuth(app)

books = []


class Book:
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
    books.append(new_book)
    return jsonify({'message': 'Book added successfully'})


@app.route('/books/<isbn>', methods=['GET'])
def get_book(isbn):
    for book in books:
        if book.isbn == isbn:
            return jsonify({
                'title': book.title,
                'author': book.author,
                'isbn': book.isbn,
                'description': book.description,
                'price': book.price
            })
    return jsonify({'message': 'Book not found'}), 404


@app.route('/books/<isbn>', methods=['PUT'])
@basic_auth.required
def update_book(isbn):
    data = request.get_json()
    for book in books:
        if book.isbn == isbn:
            if 'title' in data:
                book.title = data['title']
            if 'author' in data:
                book.author = data['author']
            if 'description' in data:
                book.description = data['description']
            if 'price' in data:
                book.price = data['price']
            return jsonify({'message': 'Book updated successfully'})
    return jsonify({'message': 'Book not found'}), 404


@app.route('/books/<isbn>', methods=['DELETE'])
@basic_auth.required
def delete_book(isbn):
    for book in books:
        if book.isbn == isbn:
            books.remove(book)
            return jsonify({'message': 'Book deleted successfully'})
    return jsonify({'message': 'Book not found'}), 404


@app.route('/books', methods=['GET'])
def list_books():
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
