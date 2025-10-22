import React from 'react';
import ChatWindow from '../components/chatWindow.jsx';

export default function Dashboard() {
  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
      <ChatWindow />
    </div>
  );
}
