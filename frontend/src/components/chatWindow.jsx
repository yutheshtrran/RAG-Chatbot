import React, { useState } from "react";
import { sendMessage } from "../api";

export default function ChatWindow() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;

    // Show user message immediately
    setMessages((prev) => [...prev, { sender: "user", text: input }]);
    setLoading(true);

    // Send to backend via API
    const reply = await sendMessage(input);
    setMessages((prev) => [...prev, { sender: "bot", text: reply }]);
    setInput("");
    setLoading(false);
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-[500px] border rounded-lg p-4 bg-white shadow-lg">
      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto space-y-3 mb-4">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`p-3 rounded-lg max-w-[80%] ${
              msg.sender === "user" ? "bg-blue-100 self-end" : "bg-gray-100 self-start"
            }`}
          >
            {msg.text}
          </div>
        ))}
        {loading && (
          <div className="p-3 rounded-lg bg-gray-100 self-start">Typing...</div>
        )}
      </div>

      {/* Input Box */}
      <div className="flex items-center gap-2">
        <input
          type="text"
          className="flex-1 border rounded-lg p-2"
          placeholder="Ask about a patient, e.g., 'Show me patient 123 history'"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
        />
        <button
          onClick={handleSend}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
        >
          Send
        </button>
      </div>
    </div>
  );
}
