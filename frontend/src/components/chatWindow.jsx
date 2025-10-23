import React, { useState, useRef, useEffect } from 'react';
import MessageBubble from './MessageBubble';
import { SendIcon, LoaderIcon } from './Icons'; 

export default function ChatWindow() {
  const [messages, setMessages] = useState([
    { id: 1, text: 'Hello! I am your AI assistant. How can I help you today?', sender: 'bot' },
    { id: 2, text: 'I need to check my recent project evaluation scores.', sender: 'user' },
    { id: 3, text: 'Sure! I can help with that. Which project are you referring to?', sender: 'bot' },
  ]);
  const [loading, setLoading] = useState(false);
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);

  // Scroll to bottom when messages update
  useEffect(() => {
    const timer = setTimeout(() => {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, 50);
    return () => clearTimeout(timer);
  }, [messages, loading]);

  // Only keep this async function
  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMessage = { id: Date.now(), text: input, sender: 'user' };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const res = await fetch('http://127.0.0.1:5000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input })
      });

      const data = await res.json();
      const botMessage = { id: Date.now() + 1, text: data.reply, sender: 'bot' };
      setMessages(prev => [...prev, botMessage]);
    } catch (err) {
      console.error(err);
      setMessages(prev => [
        ...prev,
        { id: Date.now() + 2, text: 'Sorry, something went wrong!', sender: 'bot' }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = e => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="flex flex-col h-[550px] md:h-[650px] w-full max-w-4xl mx-auto rounded-xl shadow-2xl bg-white border border-gray-100 overflow-hidden">
      
      {/* Messages Window */}
      <div className="flex-1 overflow-y-auto p-5 space-y-4 custom-scrollbar bg-gray-50/50">
        {messages.map(msg => (
          <MessageBubble key={msg.id} text={msg.text} sender={msg.sender} />
        ))}

        {loading && (
          <div className="flex items-center gap-2 self-start animate-pulse">
            <div className="bg-gray-200 p-2 rounded-full shadow-inner">
               <LoaderIcon className="w-5 h-5 text-blue-500 animate-spin" />
            </div>
            <span className="text-sm text-gray-500 italic ml-2">AI is analyzing...</span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-4 border-t border-gray-100 bg-white shadow-lg">
        <div className="flex items-center gap-3">
          <input
            type="text"
            className="flex-1 resize-none border border-gray-300 rounded-full pl-5 pr-4 py-3 text-base 
                       focus:outline-none focus:ring-4 focus:ring-blue-100 focus:border-blue-500 transition duration-150"
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={loading ? "Please wait for the response..." : "Ask me anything about your evaluations..."}
            disabled={loading}
            aria-label="Message input field"
          />
          
          <button
            className={`p-3 rounded-full flex items-center justify-center text-white transition duration-200 ease-in-out 
              ${input.trim() && !loading 
                ? 'bg-blue-600 hover:bg-blue-700 shadow-md hover:shadow-lg' 
                : 'bg-gray-400 cursor-not-allowed opacity-70'
              }`}
            onClick={sendMessage}
            disabled={!input.trim() || loading}
            aria-label="Send message"
          >
            <SendIcon className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
}
