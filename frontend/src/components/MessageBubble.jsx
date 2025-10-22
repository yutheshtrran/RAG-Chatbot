import React from 'react';

export default function MessageBubble({ text, sender }) {
  return (
    <div className={`p-2 rounded ${sender === 'user' ? 'bg-green-200 self-end' : 'bg-gray-300 self-start'}`}>
      {text}
    </div>
  );
}
