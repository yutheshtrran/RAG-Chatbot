import React from 'react';
import { GithubIcon, ExternalLinkIcon } from './Icons'; // Assuming these icons exist

export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    // The footer is now fixed at the bottom for better visibility on a dashboard layout.
    // It uses a very light gray background for subtlety.
    <footer className="w-full bg-white border-t border-gray-100 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3 flex justify-between items-center text-sm text-gray-500">
        
        {/* Left Section: Copyright & Name */}
        <div className="flex items-center space-x-4">
          <p className="font-medium text-gray-600">
            &copy; {currentYear} AI Evaluation System.
          </p>
          {/* Optional: Add a link to the project's source code if open-source */}
          <a
            href="https://github.com/your-repo" 
            target="_blank" 
            rel="noopener noreferrer" 
            className="hidden sm:inline-flex items-center hover:text-blue-600 transition duration-150"
            aria-label="View project on GitHub"
          >
            <GithubIcon className="w-4 h-4 mr-1" /> Source Code
          </a>
        </div>

        {/* Right Section: Navigation Links */}
        <nav className="flex space-x-4 md:space-x-6">
          <a 
            href="/about" 
            className="hover:text-blue-600 transition duration-150 hover:underline"
            aria-label="Navigate to the About page"
          >
            About
          </a>
          <a 
            href="/privacy" 
            className="hover:text-blue-600 transition duration-150 hover:underline"
            aria-label="View Privacy Policy"
          >
            Privacy
          </a>
          <a 
            href="/terms" 
            className="hover:text-blue-600 transition duration-150 hover:underline"
            aria-label="View Terms of Service"
          >
            Terms
          </a>
        </nav>
      </div>
    </footer>
  );
}