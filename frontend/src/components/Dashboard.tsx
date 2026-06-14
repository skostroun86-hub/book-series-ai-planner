import React from 'react';

const Dashboard: React.FC = () => {
  return (
    <div className="dashboard">
      <h2>Welcome to Book Series AI Planner</h2>
      <div className="dashboard-grid">
        <div className="dashboard-card">
          <h3>📖 Manage Your Books</h3>
          <p>Create and organize your book series with detailed information and tracking.</p>
        </div>
        <div className="dashboard-card">
          <h3>💬 AI Chat Assistant</h3>
          <p>Get help from specialized AI assistants: Story Architect, Character Psychologist, Worldbuilder, Editor, and more.</p>
        </div>
        <div className="dashboard-card">
          <h3>👥 Character Management</h3>
          <p>Create and track characters with consistency checking and relationship mapping.</p>
        </div>
        <div className="dashboard-card">
          <h3>📊 Plot & Timeline</h3>
          <p>Organize plot points and visualize your story timeline.</p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
