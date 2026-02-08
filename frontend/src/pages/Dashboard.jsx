import React, { useState } from 'react';
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

  const [showUploader, setShowUploader] = useState(false);

  const stats = [
    { title: 'Total Evaluations', value: '452', icon: EvaluationIcon, color: 'text-blue-500', bg: 'bg-blue-50' },
    { title: 'Accuracy Score', value: '98.5%', icon: CheckCircleIcon, color: 'text-green-500', bg: 'bg-green-50' },
    { title: 'Active Users', value: '24', icon: UserIcon, color: 'text-indigo-500', bg: 'bg-indigo-50' },
    { title: 'RAG Usage Trend', value: '+12%', icon: TrendingUpIcon, color: 'text-yellow-500', bg: 'bg-yellow-50' },
  ];

  return (
    <div className="p-4 sm:p-6 lg:p-8 bg-gray-50 dark:bg-slate-900 min-h-screen">

      {/* Page Header */}
      <header className="mb-6">
        <h1 className="text-3xl font-extrabold text-gray-800 dark:text-white flex items-center">
          <DashboardIcon className="w-8 h-8 mr-3 text-blue-600" />
          System Dashboard
        </h1>
        <p className="text-gray-500 dark:text-gray-300 mt-1">
          Welcome back! Here's a quick overview of system statistics and your AI assistant.
        </p>
      </header>

      {/* Upload Patient Button */}
      <div className="mb-8">
        <button
          onClick={() => setShowUploader(true)}
          className="px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg shadow hover:bg-blue-700 transition"
        >
          Upload Patient Record
        </button>
      </div>

      {/* Patient Uploader Modal */}
      {showUploader && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
          <div className="bg-white dark:bg-slate-800 rounded-xl shadow-xl w-full max-w-lg p-6 relative">

            <button
              onClick={() => setShowUploader(false)}
              className="absolute top-3 right-3 text-gray-400 hover:text-gray-600 dark:hover:text-white text-xl"
            >
              ✕
            </button>

            <h2 className="text-xl font-semibold text-gray-800 dark:text-white mb-4">
              Upload Patient Record
            </h2>

            <PatientUploader />
          </div>
        </div>
      )}

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">

        {/* Left Column */}
        <div className="lg:col-span-1 space-y-6">
          
          <h2 className="text-xl font-semibold text-gray-700 dark:text-gray-200 border-b pb-2">
            Key Metrics
          </h2>

          {/* Statistics Cards */}
          <div className="space-y-4">
            {stats.map((stat) => {
              const Icon = stat.icon;
              return (
                <div
                  key={stat.title}
                  className="p-5 bg-white dark:bg-slate-800 rounded-xl shadow-lg border border-gray-100 dark:border-slate-700"
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-500 dark:text-gray-300">
                        {stat.title}
                      </p>
                      <p className="mt-1 text-3xl font-bold text-gray-900 dark:text-white">
                        {stat.value}
                      </p>
                    </div>
                    <div className={`p-3 rounded-full ${stat.bg} ${stat.color}`}>
                      <Icon className="w-6 h-6" />
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Quick Links */}
          <div className="p-5 bg-white dark:bg-slate-800 rounded-xl shadow-lg border border-gray-100 dark:border-slate-700">
            <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-200 mb-3">
              Quick Links
            </h3>
            <ul className="space-y-2 text-sm">
              <li>
                <a href="/evaluation" className="text-blue-600 hover:text-blue-800 dark:text-blue-400">
                  View Detailed Evaluation Reports
                </a>
              </li>
              <li>
                <a href="/about" className="text-indigo-600 hover:text-indigo-800 dark:text-indigo-400">
                  Read RAG Documentation
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Right Column */}
        <div className="lg:col-span-2">
          <h2 className="text-xl font-semibold text-gray-700 dark:text-gray-200 border-b pb-2 mb-4">
            AI Clinical Assistant
          </h2>
          <ChatWindow />
        </div>

      </div>
    </div>
  );
}
