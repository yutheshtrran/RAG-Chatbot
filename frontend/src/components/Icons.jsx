import React from 'react';
// Import all necessary icons from lucide-react (or your chosen modern library)
import { 
    Send, Loader2, Menu, Bell, User, Settings, Github, LogOut, X, 
    LayoutDashboard, BarChart2, Info, CheckCircle, TrendingUp, 
    Filter, Download, Table, ChevronDown, Link as ExternalLink, 
    Activity, HeartHandshake, Shield, Search
} from 'lucide-react';

// Add at the bottom or with your other exports
export const UploadIcon = (props) => (
  <svg
    {...props}
    fill="none"
    stroke="currentColor"
    viewBox="0 0 24 24"
    xmlns="http://www.w3.org/2000/svg"
  >
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={2}
      d="M4 16v4h16v-4M12 12V4m0 0l-4 4m4-4l4 4"
    />
  </svg>
);


// --- UTILITY/GLOBAL ICONS ---

export const SearchIcon = ({ className = 'w-5 h-5' }) => (
    <Search size={20} className={className} />
);

export const ExternalLinkIcon = ({ className = 'w-4 h-4' }) => (
    <ExternalLink size={16} className={className} />
);

// --- NAVIGATION / LAYOUT ICONS ---

// Menu Icon: For toggling the mobile sidebar
export const MenuIcon = ({ className = 'w-6 h-6' }) => (
  <Menu size={24} className={className} />
);

// Close Icon: For closing the mobile sidebar
export const XIcon = ({ className = 'w-6 h-6' }) => (
    <X size={24} className={className} />
);

// User Icon: For the Header profile/avatar and Sidebar
export const UserIcon = ({ className = 'w-5 h-5' }) => (
  <User size={20} className={className} />
);

// Log Out Icon: For the Sidebar logout link
export const LogOutIcon = ({ className = 'w-5 h-5' }) => (
    <LogOut size={20} className={className} />
);

// Settings Icon: For the Header settings button
export const SettingsIcon = ({ className = 'w-6 h-6' }) => (
  <Settings size={24} className={className} />
);

// Notification Bell Icon: For the Header
export const BellIcon = ({ className = 'w-6 h-6' }) => (
  <Bell size={24} className={className} />
);

// Github Icon: For linking to the project source (in Footer)
export const GithubIcon = ({ className = 'w-4 h-4' }) => (
    <Github size={16} className={className} />
);

// --- CHAT ICONS (ChatWindow.jsx) ---

// Send Icon: Used in ChatWindow for sending messages
export const SendIcon = ({ className = 'w-5 h-5 ml-1' }) => (
  <Send size={20} className={className} />
);

// Loader Icon: Used in ChatWindow for the 'typing' indicator and Loader.jsx
export const LoaderIcon = ({ className = 'w-5 h-5 text-blue-500' }) => (
  <Loader2 size={20} className={`animate-spin ${className}`} />
);

// --- PAGE NAVIGATION ICONS (Sidebar.jsx) ---

// Dashboard Icon
export const DashboardIcon = ({ className = 'w-5 h-5' }) => (
    <LayoutDashboard size={20} className={className} />
);

// Evaluation Icon
export const EvaluationIcon = ({ className = 'w-5 h-5' }) => (
    <BarChart2 size={20} className={className} />
);

// About Icon
export const InfoIcon = ({ className = 'w-5 h-5' }) => (
    <Info size={20} className={className} />
);

// --- DASHBOARD STATS ICONS (Dashboard.jsx) ---

// Success/Check Icon
export const CheckCircleIcon = ({ className = 'w-6 h-6' }) => (
    <CheckCircle size={24} className={className} />
);

// Trend Icon
export const TrendingUpIcon = ({ className = 'w-6 h-6' }) => (
    <TrendingUp size={24} className={className} />
);

// --- EVALUATION PAGE ICONS (Evaluation.jsx) ---

// Chart Icon
export const BarChart2Icon = ({ className = 'w-5 h-5' }) => (
    <BarChart2 size={20} className={className} />
);

// Table Icon
export const TableIcon = ({ className = 'w-5 h-5' }) => (
    <Table size={20} className={className} />
);

// Filter Icon
export const FilterIcon = ({ className = 'w-5 h-5' }) => (
    <Filter size={20} className={className} />
);

// Download Icon
export const DownloadIcon = ({ className = 'w-5 h-5' }) => (
    <Download size={20} className={className} />
);

// Chevron Down Icon (for dropdowns)
export const ChevronDownIcon = ({ className = 'w-4 h-4' }) => (
    <ChevronDown size={16} className={className} />
);

// --- ABOUT PAGE ICONS (About.jsx) ---

// Shield Icon (for accuracy/security)
export const ShieldIcon = ({ className = 'w-6 h-6' }) => (
    <Shield size={24} className={className} />
);

// Handshake/Trust Icon (for compliance/focus)
export const HeartHandshakeIcon = ({ className = 'w-6 h-6' }) => (
    <HeartHandshake size={24} className={className} />
);

// Activity/System Icon (for technology/metrics)
export const ActivityIcon = ({ className = 'w-6 h-6' }) => (
    <Activity size={24} className={className} />
);