import React from 'react';
import { X } from './Icons.jsx'; // Explicitly set extension to resolve path issue

/**
 * Sidebar Component
 * Provides navigation and context for the application.
 */
const Sidebar = ({ isSidebarOpen, setIsSidebarOpen, activePage, setActivePage }) => {
    const navItems = [
        { name: 'Dashboard', icon: '⚡' },
        { name: 'Evaluation', icon: '📊' },
        { name: 'About', icon: 'ℹ️' },
    ];

    return (
        <div className={`fixed inset-y-0 left-0 z-40 transform bg-white border-r border-gray-200 shadow-xl transition-transform duration-300 ease-in-out lg:translate-x-0 ${isSidebarOpen ? 'translate-x-0' : '-translate-x-full'} w-64`}>
            <div className="h-full flex flex-col p-4">
                <div className="flex justify-between items-center mb-6">
                    <h2 className="text-xl font-bold text-indigo-700">Medical RAG</h2>
                    <button
                        onClick={() => setIsSidebarOpen(false)}
                        className="text-gray-500 hover:text-indigo-600 lg:hidden p-1 rounded-full transition-colors"
                        aria-label="Close sidebar"
                    >
                        <X className="w-6 h-6" />
                    </button>
                </div>
                
                <nav className="space-y-2 flex-grow">
                    {navItems.map((item) => (
                        <button
                            key={item.name}
                            onClick={() => {
                                setActivePage(item.name);
                                setIsSidebarOpen(false); // Close on mobile
                            }}
                            className={`flex items-center w-full p-3 rounded-lg transition-colors duration-200 text-left ${
                                activePage === item.name
                                    ? 'bg-indigo-100 text-indigo-700 font-semibold shadow-sm'
                                    : 'text-gray-600 hover:bg-gray-50 hover:text-indigo-600'
                            }`}
                        >
                            <span className="mr-3 text-lg">{item.icon}</span>
                            {item.name}
                        </button>
                    ))}
                </nav>

                <div className="mt-auto pt-4 border-t border-gray-100">
                    <p className="text-xs text-gray-400">v1.0.0 | Context: Clinical Data</p>
                </div>
            </div>
        </div>
    );
};

export default Sidebar;
