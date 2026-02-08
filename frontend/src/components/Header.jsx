import React from 'react';
import { MenuIcon, BellIcon, UserIcon, SettingsIcon, SunIcon, MoonIcon } from './Icons'; 
import { useTheme } from '../context/ThemeContext';

export default function Header({ onMenuClick }) {
  const { isDark, toggleTheme } = useTheme();

  return (
    <header className="sticky top-0 z-30 w-full bg-white dark:bg-slate-900 shadow-lg border-b border-gray-100 dark:border-slate-700 transition-colors duration-200">
      <div className="max-w-full mx-auto px-4 sm:px-6 lg:px-8 h-16 flex justify-between items-center">
        
        {/* Left Section: Logo/Brand and Sidebar Toggle */}
        <div className="flex items-center space-x-4">
          
          {/* Menu Button (for Mobile/Collapsed Sidebar) */}
          <button
            onClick={onMenuClick}
            className="p-2 rounded-full text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-slate-800 hover:text-blue-600 dark:hover:text-blue-400 transition lg:hidden"
            aria-label="Toggle navigation menu"
          >
            <MenuIcon className="w-6 h-6" />
          </button>

          {/* Application Title/Logo */}
          <div className="text-2xl font-extrabold text-gray-800 dark:text-white tracking-tight">
            <span className="text-blue-600">RAG</span> Clinical Assistant
          </div>

          {/* Primary Navigation (Desktop Only) */}
          <nav className="hidden lg:flex ml-10 space-x-8 text-sm font-medium">
            <a href="/dashboard" className="text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition border-b-2 border-transparent hover:border-blue-600 dark:hover:border-blue-400 pb-1">
              Dashboard
            </a>
            <a href="/evaluation" className="text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition border-b-2 border-transparent hover:border-blue-600 dark:hover:border-blue-400 pb-1">
              Evaluations
            </a>
            <a href="/about" className="text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition border-b-2 border-transparent hover:border-blue-600 dark:hover:border-blue-400 pb-1">
              About
            </a>
          </nav>
        </div>

        {/* Right Section: Actions and User Profile */}
        <div className="flex items-center space-x-3 sm:space-x-4">
          
          {/* Notifications Button */}
          <button
            className="p-2 rounded-full text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-slate-800 hover:text-blue-600 dark:hover:text-blue-400 transition relative"
            aria-label="View notifications"
          >
            <BellIcon className="w-6 h-6" />
            <span className="absolute top-1 right-1 block h-2 w-2 rounded-full ring-2 ring-white dark:ring-slate-900 bg-red-500" aria-hidden="true" />
          </button>

          {/* Theme Toggle Button */}
          <button
            onClick={toggleTheme}
            className="p-2 rounded-full text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-slate-800 hover:text-blue-600 dark:hover:text-blue-400 transition"
            aria-label="Toggle theme"
          >
            {isDark ? <SunIcon className="w-6 h-6" /> : <MoonIcon className="w-6 h-6" />}
          </button>

          {/* Settings Button */}
          <button
            className="hidden sm:block p-2 rounded-full text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-slate-800 hover:text-blue-600 dark:hover:text-blue-400 transition"
            aria-label="Open settings"
          >
            <SettingsIcon className="w-6 h-6" />
          </button>

          {/* User Profile / Avatar */}
          <button
            className="flex items-center justify-center w-8 h-8 rounded-full bg-blue-500 dark:bg-blue-600 text-white font-semibold shadow-sm hover:ring-2 hover:ring-blue-300 dark:hover:ring-blue-400 transition"
            aria-label="Open user menu"
          >
            {/* Example: Display first letter of user name or an icon */}
            <UserIcon className="w-5 h-5" />
          </button>
        </div>
      </div>
    </header>
  );
}