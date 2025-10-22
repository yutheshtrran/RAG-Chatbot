import React, { useState, useRef, useEffect } from 'react';
import MessageBubble from './MessageBubble';
import { SendIcon, LoaderIcon } from './Icons';

export default function ChatWindow() {
  const [messages, setMessages] = useState([
    { id: 1, text: 'Hello! How can I help you today?', sender: 'bot' },
  ]);
  const [loading, setLoading] = useState(false);
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);

  // Scroll to bottom when messages update
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const sendMessage = () => {
    if (!input.trim()) return;

    // Add user message
    const userMessage = { id: Date.now(), text: input, sender: 'user' };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    // Simulate bot response
    setTimeout(() => {
      const botMessage = {
        id: Date.now() + 1,
        text: 'This is a bot reply.',
        sender: 'bot',
      };
      setMessages(prev => [...prev, botMessage]);
      setLoading(false);
    }, 1000);
  };

  const handleKeyDown = e => {
    if (e.key === 'Enter') sendMessage();
  };

  return (
    <div className="flex flex-col h-96 border rounded-lg p-4 bg-white shadow-md">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto flex flex-col gap-2">
        {messages.map(msg => (
          <MessageBubble key={msg.id} text={msg.text} sender={msg.sender} />
        ))}
        {loading && (
          <div className="flex items-center gap-2 self-start">
            <LoaderIcon />
            <span className="text-gray-500 italic">Bot is typing...</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="mt-4 flex gap-2">
        <input
          type="text"
          className="flex-1 border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type your message..."
        />
        <button
          className="bg-blue-500 text-white px-4 py-2 rounded flex items-center hover:bg-blue-600 transition"
          onClick={sendMessage}
        >
          Send <SendIcon />
        </button>
      </div>
    </div>
  );
}
