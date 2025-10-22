import React from 'react';
// Import updated, consistent icon components from icons.jsx
import { XIcon, DashboardIcon, EvaluationIcon, AboutIcon, UserIcon, LogOutIcon } from './Icons'; 
// Note: We rename 'X' to 'XIcon' and assume LogOutIcon is also available in Icons.jsx (e.g., from 'LogOut' in lucide)

/**
 * Sidebar Component
 * Provides navigation and context for the application.
 */
const Sidebar = ({ isSidebarOpen, setIsSidebarOpen, activePage, setActivePage, userName = 'Dr. Alex Lee' }) => {
    
    // Use proper icon components instead of emojis for a professional look
    const navItems = [
        { name: 'Dashboard', icon: DashboardIcon, href: '/dashboard' },
        { name: 'Evaluation', icon: EvaluationIcon, href: '/evaluation' },
        { name: 'About', icon: AboutIcon, href: '/about' },
    ];

    return (
        <>
            {/* 1. Mobile Overlay (Darkens background when sidebar is open on small screens) */}
            {isSidebarOpen && (
                <div 
                    className="fixed inset-0 bg-gray-900/50 z-30 lg:hidden"
                    onClick={() => setIsSidebarOpen(false)}
                    aria-hidden="true"
                />
            )}

            {/* 2. Sidebar Container */}
            <div className={`
                fixed inset-y-0 left-0 z-40 w-64
                transform bg-white border-r border-gray-100 shadow-2xl 
                transition-transform duration-300 ease-in-out
                lg:translate-x-0 lg:shadow-xl
                ${isSidebarOpen ? 'translate-x-0' : '-translate-x-full'}
            `}>
                <div className="h-full flex flex-col p-6">
                    
                    {/* Top Section: Logo/Branding and Close Button */}
                    <div className="flex justify-between items-center mb-8">
                        {/* Enhanced Branding */}
                        <h2 className="text-2xl font-extrabold tracking-tight text-gray-800">
                            <span className="text-blue-600">Medi</span><span className="font-light text-indigo-700">RAG</span>
                        </h2>
                        {/* Close Button for Mobile */}
                        <button
                            onClick={() => setIsSidebarOpen(false)}
                            className="text-gray-400 hover:text-blue-600 lg:hidden p-1 rounded-full hover:bg-gray-100 transition-colors"
                            aria-label="Close sidebar"
                        >
                            <XIcon className="w-6 h-6" />
                        </button>
                    </div>
                    
                    {/* Navigation Links */}
                    <nav className="space-y-2 flex-grow">
                        {navItems.map((item) => {
                            const Icon = item.icon; // Get the component
                            const isActive = activePage === item.name;

                            return (
                                <a // Changed from button to 'a' tag for semantic navigation, use 'href'
                                    key={item.name}
                                    href={item.href} // Use href for real navigation or history/router pushes
                                    onClick={(e) => {
                                        e.preventDefault(); // Prevent default link behavior for SPA routing
                                        setActivePage(item.name);
                                        setIsSidebarOpen(false); // Close on mobile
                                    }}
                                    className={`
                                        flex items-center w-full p-3 rounded-xl transition-all duration-200 text-base
                                        ${isActive
                                            ? 'bg-blue-600 text-white font-semibold shadow-lg hover:bg-blue-700'
                                            : 'text-gray-700 hover:bg-gray-100 hover:text-blue-600'
                                        }`}
                                >
                                    <Icon className={`mr-4 ${isActive ? 'text-white' : 'text-gray-500'}`} />
                                    {item.name}
                                </a>
                            );
                        })}
                    </nav>

                    {/* Bottom Section: User Profile and Logout */}
                    <div className="mt-8 pt-4 border-t border-gray-200">
                        {/* User Card */}
                        <div className="flex items-center p-3 rounded-xl bg-gray-50 mb-4 cursor-pointer hover:bg-gray-100 transition">
                            <div className="w-10 h-10 flex items-center justify-center rounded-full bg-blue-500 text-white font-semibold flex-shrink-0">
                                {userName.charAt(0)}
                            </div>
                            <div className="ml-3 truncate">
                                <p className="text-sm font-semibold text-gray-800 truncate">{userName}</p>
                                <p className="text-xs text-gray-500">View Profile</p>
                            </div>
                        </div>

                        {/* Logout/Version Info */}
                        <a 
                            href="/logout" 
                            className="flex items-center w-full p-3 rounded-xl text-sm text-red-500 hover:bg-red-50 hover:text-red-700 transition"
                        >
                            <LogOutIcon className="w-5 h-5 mr-3" />
                            Log Out
                        </a>
                        <p className="mt-4 text-xs text-gray-400">
                            v1.0.0 | Context: Clinical Data
                        </p>
                    </div>
                </div>
            </div>
        </>
    );
};

export default Sidebar;