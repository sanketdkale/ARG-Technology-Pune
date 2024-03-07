from flask import Flask, request, jsonify

app = Flask(__name__)

books = []


def handle_error(f):
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    wrapper.__name__ = f.__name__
    return wrapper


@app.route('/books', methods=['POST'])
@handle_error
def create_books():
    data = request.json
    if not isinstance(data, list):
        return jsonify({'error': 'Request body should be a JSON array of books'}), 400

    for book_data in data:
        required_fields = ['title', 'author', 'isbn', 'description', 'price']
        for field in required_fields:
            if field not in book_data:
                return jsonify({'error': f'Missing required field in one of the books: {field}'}), 400
        if any(book['isbn'] == book_data['isbn'] for book in books):
            return jsonify({'error': f'Book with the same ISBN already exists: {book_data["isbn"]}'}), 400

    for book_data in data:
        books.append(book_data)

    return jsonify({'message': f'{len(data)} books added successfully'}), 201


@app.route('/books/<isbn>', methods=['GET'])
@handle_error
def retrieve_book(isbn):
    book = next((book for book in books if book['isbn'] == isbn), None)
    if book is None:
        return jsonify({'error': 'Book not found'}), 404
    return jsonify(book)


@app.route('/books/<isbn>', methods=['PUT'])
@handle_error
def update_book(isbn):
    data = request.json
    if not isinstance(data, list):
        return jsonify({'error': 'Request body should be a JSON array of books'}), 400

    updated_books = 0
    for updated_book in data:
        book = next((book for book in books if book['isbn'] == isbn), None)
        if book is None:
            return jsonify({'error': f'Book with ISBN {isbn} not found'}), 404
        for key, value in updated_book.items():
            if key in book:
                book[key] = value
        updated_books += 1

    return jsonify({'message': f'{updated_books} books updated successfully'}), 200


@app.route('/books/<isbn>', methods=['DELETE'])
@handle_error
def delete_book(isbn):
    global books
    books = [book for book in books if book['isbn'] != isbn]
    return jsonify({'message': 'Book deleted successfully'})


# List All Books
@app.route('/books', methods=['GET'])
@handle_error
def list_books():
    return jsonify(books)


if __name__ == '__main__':
    app.run(debug=True)
