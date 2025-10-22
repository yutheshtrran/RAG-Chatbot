import React from 'react';
import { LoaderIcon } from './Icons'; 
// Assuming LoaderIcon is imported from icons.jsx and handles the spinning animation

/**
 * A visually enhanced loader component for displaying loading status.
 * It features a spinning icon and clear text feedback.
 */
export default function Loader({ text = 'Loading data, please wait...' }) {
  return (
    // Centering the loader and making it prominent (useful for full-page or large block loading)
    <div className="flex flex-col items-center justify-center p-8 bg-white/70 backdrop-blur-sm rounded-lg shadow-inner w-full h-full min-h-[150px]">
      
      {/* Spinning Icon */}
      {/* We use the custom LoaderIcon and make it large and prominent */}
      <LoaderIcon className="w-8 h-8 text-blue-600 animate-spin mb-3" />
      
      {/* Loading Text */}
      <p className="text-lg font-medium text-gray-700 animate-pulse">
        {text}
      </p>

      {/* Optional: Add a small detail below the text */}
      <div className="mt-2 text-xs text-gray-500">
        Working hard to fetch your content...
      </div>
    </div>
  );
}