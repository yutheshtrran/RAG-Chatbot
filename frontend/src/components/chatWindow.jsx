import React, { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import { sendMessage } from "../api";
import Loader from "./Loader";

export default function ChatWindow() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = input;
    setInput("");

    // Show user message immediately
    setMessages((prev) => [...prev, { sender: "user", text: userMessage }]);
    setLoading(true);

    // Send to backend via API
    const reply = await sendMessage(userMessage);
    setMessages((prev) => [...prev, { sender: "bot", text: reply }]);
    setLoading(false);
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-[600px] border border-gray-300 dark:border-slate-700 rounded-lg p-4 bg-white dark:bg-slate-800 shadow-lg">
      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto space-y-4 mb-4 bg-gray-50 dark:bg-slate-900 rounded-lg p-3">
        {messages.length === 0 && !loading && (
          <div className="flex items-center justify-center h-full text-gray-400 dark:text-gray-400">
            <p className="text-center">
              👋 Welcome! Start by asking a question about a patient.<br/>
              <span className="text-sm">Example: "Patient 001 what is their diagnosis?"</span>
            </p>
          </div>
        )}

        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex ${msg.sender === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
            className={`max-w-[75%] p-4 rounded-lg ${
                msg.sender === "user"
                  ? "bg-blue-600 text-white rounded-br-none"
                  : "bg-gray-200 dark:bg-slate-700 text-gray-900 dark:text-gray-100 rounded-bl-none"
              }`}
            >
              {msg.sender === "bot" ? (
                <div className="prose prose-sm max-w-none">
                  <ReactMarkdown
                    components={{
                      p: ({ node, ...props }) => <p className="mb-2 last:mb-0" {...props} />,
                      ul: ({ node, ...props }) => <ul className="list-disc list-inside mb-2" {...props} />,
                      ol: ({ node, ...props }) => <ol className="list-decimal list-inside mb-2" {...props} />,
                      li: ({ node, ...props }) => <li className="mb-1" {...props} />,
                      strong: ({ node, ...props }) => <strong className="font-semibold" {...props} />,
                      em: ({ node, ...props }) => <em className="italic" {...props} />,
                      code: ({ node, inline, ...props }) => (
                        inline ? (
                          <code className="bg-gray-300 px-1.5 py-0.5 rounded text-xs font-mono" {...props} />
                        ) : (
                          <code className="block bg-gray-300 p-2 rounded text-xs font-mono overflow-x-auto" {...props} />
                        )
                      ),
                      h1: ({ node, ...props }) => <h1 className="text-lg font-bold mb-2" {...props} />,
                      h2: ({ node, ...props }) => <h2 className="text-base font-bold mb-2" {...props} />,
                      h3: ({ node, ...props }) => <h3 className="text-sm font-bold mb-1" {...props} />,
                    }}
                  >
                    {msg.text}
                  </ReactMarkdown>
                </div>
              ) : (
                <p className="whitespace-pre-wrap break-words">{msg.text}</p>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex justify-start">
            <div className="max-w-[75%] p-4 rounded-lg bg-gray-200 text-gray-900 rounded-bl-none">
              <Loader />
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Box */}
      <div className="flex items-center gap-2 border-t border-gray-200 dark:border-slate-700 pt-3">
        <textarea
          className="flex-1 border border-gray-300 dark:border-slate-600 rounded-lg p-2 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white dark:bg-slate-900 text-gray-900 dark:text-gray-100"
          placeholder="Ask a question about a patient (e.g., 'Patient 001 what is their medical history?')"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          rows="2"
          disabled={loading}
        />
        <button
          onClick={handleSend}
          disabled={loading || !input.trim()}
          className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition"
        >
          Send
        </button>
      </div>
    </div>
  );
}

