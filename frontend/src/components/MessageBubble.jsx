import React from 'react';
import { UserIcon } from './Icons'; // Assuming UserIcon for user avatar, and we'll use a simple letter for bot/AI

export default function MessageBubble({ text, sender }) {
  // Determine alignment, colors, and shadow based on the sender
  const isUser = sender === 'user';
  
  const bubbleClasses = isUser
    ? // USER Bubble (Right Aligned, Primary Color, Stronger Shadow)
      'bg-blue-600 text-white self-end rounded-t-xl rounded-bl-xl shadow-md'
    : // BOT Bubble (Left Aligned, Subtle Background, Soft Shadow)
      'bg-white text-gray-800 self-start rounded-t-xl rounded-br-xl shadow-lg border border-gray-100';

  // Determine avatar/timestamp container alignment
  const containerAlignment = isUser ? 'justify-end' : 'justify-start';

  return (
    // Outer container for alignment and full width control
    <div className={`flex w-full ${containerAlignment}`}>
      
      {/* Bot Avatar (only visible for bot messages) */}
      {!isUser && (
        <div className="flex-shrink-0 mr-3 mt-1">
          {/* Simple Bot Avatar (B for Bot/Brand) */}
          <div className="w-8 h-8 flex items-center justify-center rounded-full bg-indigo-500 text-white font-bold text-sm">
            AI
          </div>
        </div>
      )}

      {/* Message Content */}
      <div className="flex flex-col max-w-xs sm:max-w-md">
        <div
          // Apply dynamic classes for styling and corner rounding
          className={`px-4 py-3 text-sm transition duration-300 ease-in-out ${bubbleClasses}`}
          style={{ overflowWrap: 'break-word' }} // Ensure long words wrap
        >
          {text}
        </div>

        {/* Optional: Timestamp/Read status (Placeholder) */}
        <div className={`text-xs mt-1 text-gray-400 ${isUser ? 'text-right pr-1' : 'text-left pl-1'}`}>
          {isUser ? 'Sent 5m ago' : 'Received now'}
        </div>
      </div>

      {/* User Avatar (only visible for user messages) */}
      {isUser && (
        <div className="flex-shrink-0 ml-3 mt-1">
          {/* Using the standard UserIcon for a cleaner look, or replace with user's initial/image */}
          <div className="w-8 h-8 flex items-center justify-center rounded-full bg-blue-500 text-white">
            <UserIcon className="w-4 h-4" />
          </div>
        </div>
      )}

    </div>
  );
}