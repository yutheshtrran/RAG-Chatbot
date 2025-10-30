import React, { useState, useRef, useEffect } from 'react';

// --- Icon Components (Lucide Icons for simplicity) ---
const SendIcon = (props) => (
  <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-send">
    <path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/>
  </svg>
);

const LoaderIcon = (props) => (
  <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-loader-2">
    <path d="M21 12a9 9 0 1 1-6.219-8.56"/>
  </svg>
);

// --- MessageBubble Component ---
// This ensures that only the string 'text' is rendered as a child.
const MessageBubble = ({ text, sender }) => {
  const isUser = sender === 'user';
  
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div 
        className={`max-w-xs md:max-w-md lg:max-w-lg p-3 rounded-xl shadow-md 
          ${isUser 
            ? 'bg-blue-500 text-white rounded-br-none' 
            : 'bg-white text-gray-800 rounded-tl-none border border-gray-200'
          }`}
        style={{ overflowWrap: 'break-word' }}
      >
        {/* CRITICAL: Ensure 'text' is a string before rendering */}
        <p className="text-sm sm:text-base whitespace-pre-wrap">
          {typeof text === 'string' ? text : JSON.stringify(text)}
        </p>
      </div>
    </div>
  );
};

// --- Main ChatWindow Component ---
export default function App() {
  // Renamed to App for default export, standard React convention
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
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' });
    }, 50);
    return () => clearTimeout(timer);
  }, [messages, loading]);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMessage = { id: Date.now(), text: input, sender: 'user' };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    const messageToSend = input;
    
    // Simulating API call response structure: { reply: "..." }
    const FAKE_API_ENDPOINT = 'https://jsonplaceholder.typicode.com/todos/1'; 
    const isMocking = true; // Use a mock response to run without a backend

    try {
      let botResponseText;

      if (isMocking) {
        // Mocking a successful RAG response with a delay
        await new Promise(resolve => setTimeout(resolve, 1500));
        const mockData = { reply: `I see you asked about: "${messageToSend}". For the 'Space-Time Analyzer' project, your score was 92% in logic and 88% in documentation.` };
        botResponseText = mockData.reply;

      } else {
        // REAL API CALL (uses your specified endpoint)
        const res = await fetch('http://127.0.0.1:5000/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: messageToSend })
        });

        // The critical fix is already implemented here: data.reply
        const data = await res.json();
        // Fallback safety check: ensure data.reply exists and is a string
        if (data && typeof data.reply === 'string') {
          botResponseText = data.reply;
        } else {
          // Fallback if data structure is unexpected
          throw new Error("Invalid response format from API.");
        }
      }

      const botMessage = { id: Date.now() + 1, text: botResponseText, sender: 'bot' };
      setMessages(prev => [...prev, botMessage]);

    } catch (err) {
      console.error("API or Logic Error:", err);
      setMessages(prev => [
        ...prev,
        { id: Date.now() + 2, text: `[Error: Unable to fetch response. Please check the console.] ${err.message}`, sender: 'bot' }
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
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <div className="flex flex-col h-[550px] md:h-[650px] w-full max-w-4xl mx-auto rounded-xl shadow-2xl bg-white border border-gray-100 overflow-hidden">
        
        {/* Header */}
        <div className="p-4 bg-blue-600 text-white shadow-lg">
          <h1 className="text-xl font-bold">RAG Assistant Chat</h1>
          <p className="text-sm opacity-80">Connected to Mock API for demonstration.</p>
        </div>

        {/* Messages Window */}
        <div className="flex-1 overflow-y-auto p-5 space-y-4 custom-scrollbar bg-gray-50/50">
          {messages.map(msg => (
            <MessageBubble key={msg.id} text={msg.text} sender={msg.sender} />
          ))}

          {loading && (
            <div className="flex items-center gap-2 self-start">
              <div className="bg-gray-200 p-2 rounded-full shadow-inner">
                 <LoaderIcon className="w-5 h-5 text-blue-500 animate-spin" />
              </div>
              <span className="text-sm text-gray-500 italic ml-2">AI is analyzing...</span>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="p-4 border-t border-gray-200 bg-white shadow-lg">
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
    </div>
  );
}
