import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface Book {
  id: string;
  title: string;
  description: string;
  genre: string;
  status: string;
  word_count: number;
  target_word_count: number;
}

const BookManager: React.FC = () => {
  const [books, setBooks] = useState<Book[]>([]);
  const [newBook, setNewBook] = useState({ title: '', description: '', genre: '' });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadBooks();
  }, []);

  const loadBooks = async () => {
    try {
      const response = await axios.get(`${process.env.REACT_APP_API_URL}/api/books`);
      setBooks(response.data);
    } catch (error) {
      console.error('Error loading books:', error);
    }
  };

  const handleCreateBook = async () => {
    if (!newBook.title) return;

    setLoading(true);
    try {
      await axios.post(`${process.env.REACT_APP_API_URL}/api/books`, newBook);
      setNewBook({ title: '', description: '', genre: '' });
      loadBooks();
    } catch (error) {
      console.error('Error creating book:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="book-manager">
      <h2>Book Manager</h2>

      <div className="new-book-form">
        <input
          type="text"
          placeholder="Book Title"
          value={newBook.title}
          onChange={(e) => setNewBook({ ...newBook, title: e.target.value })}
        />
        <input
          type="text"
          placeholder="Genre"
          value={newBook.genre}
          onChange={(e) => setNewBook({ ...newBook, genre: e.target.value })}
        />
        <textarea
          placeholder="Description"
          value={newBook.description}
          onChange={(e) => setNewBook({ ...newBook, description: e.target.value })}
        />
        <button onClick={handleCreateBook} disabled={loading}>
          Create Book
        </button>
      </div>

      <div className="books-list">
        {books.map((book) => (
          <div key={book.id} className="book-card">
            <h3>{book.title}</h3>
            <p className="genre">{book.genre}</p>
            <p className="description">{book.description}</p>
            <div className="book-stats">
              <span>Status: {book.status}</span>
              <span>Words: {book.word_count}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default BookManager;
