import React, { useState } from 'react';
import ChatInterface from './components/ChatInterface';
import BookManager from './components/BookManager';
import Dashboard from './components/Dashboard';
import './App.css';

type Page = 'dashboard' | 'chat' | 'books' | 'characters';

function App() {
  const [currentPage, setCurrentPage] = useState<Page>('dashboard');

  return (
    <div className="app">
      <header className="app-header">
        <h1>📚 Book Series AI Planner</h1>
        <nav>
          <button onClick={() => setCurrentPage('dashboard')}>Dashboard</button>
          <button onClick={() => setCurrentPage('chat')}>Chat</button>
          <button onClick={() => setCurrentPage('books')}>Books</button>
          <button onClick={() => setCurrentPage('characters')}>Characters</button>
        </nav>
      </header>

      <main className="app-main">
        {currentPage === 'dashboard' && <Dashboard />}
        {currentPage === 'chat' && <ChatInterface />}
        {currentPage === 'books' && <BookManager />}
        {currentPage === 'characters' && <div>Characters page coming soon</div>}
      </main>
    </div>
  );
}

export default App;
