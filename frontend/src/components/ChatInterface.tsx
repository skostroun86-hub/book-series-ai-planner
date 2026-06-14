import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [conversationId] = useState(`conv_${Date.now()}`);
  const [role, setRole] = useState('story_architect');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!input.trim()) return;

    // Add user message
    const userMessage: Message = {
      id: `msg_${Date.now()}`,
      role: 'user',
      content: input,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await axios.post(
        `${process.env.REACT_APP_API_URL}/api/chat/message`,
        {
          conversation_id: conversationId,
          message: input,
        }
      );

      const assistantMessage: Message = {
        id: response.data.message_id,
        role: 'assistant',
        content: response.data.response,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleRoleChange = async (newRole: string) => {
    try {
      await axios.post(
        `${process.env.REACT_APP_API_URL}/api/chat/role`,
        null,
        {
          params: {
            conversation_id: conversationId,
            role: newRole,
          },
        }
      );
      setRole(newRole);
    } catch (error) {
      console.error('Error changing role:', error);
    }
  };

  const roles = [
    'story_architect',
    'character_psychologist',
    'worldbuilder',
    'editor',
    'brainstormer',
    'writing_coach',
  ];

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <h2>AI Chat Assistant</h2>
        <select value={role} onChange={(e) => handleRoleChange(e.target.value)}>
          {roles.map((r) => (
            <option key={r} value={r}>
              {r.replace(/_/g, ' ').toUpperCase()}
            </option>
          ))}
        </select>
      </div>

      <div className="chat-messages">
        {messages.map((msg) => (
          <div key={msg.id} className={`message message-${msg.role}`}>
            <div className="message-role">{msg.role.toUpperCase()}</div>
            <div className="message-content">{msg.content}</div>
          </div>
        ))}
        {loading && <div className="message-loading">AI is thinking...</div>}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
          placeholder="Type your message..."
          disabled={loading}
        />
        <button onClick={handleSendMessage} disabled={loading}>
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatInterface;
