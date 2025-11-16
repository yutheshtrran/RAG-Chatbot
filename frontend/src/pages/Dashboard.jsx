import React from 'react';
import ChatWindow from '../components/ChatWindow'; 
import { 
  DashboardIcon, 
  EvaluationIcon, 
  UserIcon, 
  CheckCircleIcon, 
  TrendingUpIcon 
} from '../components/Icons'; 

import PatientUploader from '../components/PatientUploader';

/**
 * Enhanced Dashboard Component
 * Provides an overview, key statistics, and the primary chat interface.
 */
export default function Dashboard() {

  // Placeholder Data for demonstration
  const stats = [
    { title: 'Total Evaluations', value: '452', icon: EvaluationIcon, color: 'text-blue-500', bg: 'bg-blue-50' },
    { title: 'Accuracy Score', value: '98.5%', icon: CheckCircleIcon, color: 'text-green-500', bg: 'bg-green-50' },
    { title: 'Active Users', value: '24', icon: UserIcon, color: 'text-indigo-500', bg: 'bg-indigo-50' },
    { title: 'RAG Usage Trend', value: '+12%', icon: TrendingUpIcon, color: 'text-yellow-500', bg: 'bg-yellow-50' },
  ];

  return (
    <div className="p-4 sm:p-6 lg:p-8 bg-gray-50 min-h-screen">

      {/* Page Header */}
      <header className="mb-8">
        <h1 className="text-3xl font-extrabold text-gray-800 flex items-center">
          <DashboardIcon className="w-8 h-8 mr-3 text-blue-600" />
          System Dashboard
        </h1>
        <p className="text-gray-500 mt-1">
          Welcome back! Here's a quick overview of system statistics and your AI assistant.
        </p>
      </header>

      {/* Patient Uploader */}
      <PatientUploader />

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">

        {/* Left Column */}
        <div className="lg:col-span-1 space-y-6">
          
          <h2 className="text-xl font-semibold text-gray-700 border-b pb-2">Key Metrics</h2>

          {/* Statistics Cards */}
          <div className="space-y-4">
            {stats.map((stat) => {
              const Icon = stat.icon;
              return (
                <div
                  key={stat.title}
                  className="p-5 bg-white rounded-xl shadow-lg border border-gray-100 transition duration-300 hover:shadow-xl"
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-gray-500 truncate">{stat.title}</p>
                      <p className="mt-1 text-3xl font-bold text-gray-900">{stat.value}</p>
                    </div>
                    <div className={`p-3 rounded-full ${stat.bg} ${stat.color} shadow-inner`}>
                      <Icon className="w-6 h-6" />
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Quick Links */}
          <div className="p-5 bg-white rounded-xl shadow-lg border border-gray-100">
            <h3 className="text-lg font-semibold text-gray-700 mb-3">Quick Links</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <a href="/evaluation" className="text-blue-600 hover:text-blue-800 transition flex items-center">
                  <EvaluationIcon className="w-4 h-4 mr-2" />
                  View Detailed Evaluation Reports
                </a>
              </li>
              <li>
                <a href="/about" className="text-indigo-600 hover:text-indigo-800 transition flex items-center">
                  <DashboardIcon className="w-4 h-4 mr-2" />
                  Read RAG Documentation
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Right Column */}
        <div className="lg:col-span-2">
          <h2 className="text-xl font-semibold text-gray-700 border-b pb-2 mb-4">
            AI Clinical Assistant
          </h2>

          <ChatWindow />
        </div>

      </div>
    </div>
  );
}
