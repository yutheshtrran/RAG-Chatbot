import React, { useState } from 'react';
// Assuming Icons.jsx includes relevant icons like Filter, Search, Download, and Chart/Table icons
import { EvaluationIcon, FilterIcon, SearchIcon, DownloadIcon, BarChart2Icon, TableIcon, ChevronDownIcon } from '../components/Icons'; 

export default function Evaluation() {
  const [viewMode, setViewMode] = useState('chart'); // 'chart' or 'table'
  const [selectedProject, setSelectedProject] = useState('All Projects');

  // Placeholder data for filters/options
  const projects = ['All Projects', 'Clinical Trial A', 'Diagnostic Model V2', 'RAG Accuracy Report'];
  const filters = [
    { label: 'Date Range', default: 'Last 30 Days' },
    { label: 'Model Version', default: 'Latest' },
    { label: 'Evaluation Type', default: 'RAG Performance' },
  ];

  return (
    <div className="p-4 sm:p-6 lg:p-8 bg-gray-50 dark:bg-slate-900 min-h-screen">
      
      {/* Page Header */}
      <header className="mb-8 flex items-center justify-between">
        <div className="flex items-center">
          <EvaluationIcon className="w-8 h-8 mr-3 text-blue-600 dark:text-blue-400" />
          <h1 className="text-3xl font-extrabold text-gray-800 dark:text-white tracking-tight">
            Evaluation Reports
          </h1>
        </div>
        
        {/* Actions (Download Report) */}
        <button 
          className="bg-green-500 text-white px-4 py-2 rounded-lg shadow-md hover:bg-green-600 dark:bg-green-600 dark:hover:bg-green-700 transition flex items-center text-sm font-semibold"
          aria-label="Download Full Report"
        >
          <DownloadIcon className="w-5 h-5 mr-2" />
          Download Report
        </button>
      </header>

      {/* Main Content Area: Filters and Results */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        
        {/* Left Column (Filters/Controls) - Takes 1/4 width */}
        <aside className="lg:col-span-1 bg-white dark:bg-slate-800 p-6 rounded-xl shadow-lg border border-gray-100 dark:border-slate-700 h-fit sticky top-20">
          <div className="flex items-center justify-between border-b pb-3 mb-4">
            <h2 className="text-lg font-semibold text-gray-700 dark:text-gray-200 flex items-center">
              <FilterIcon className="w-5 h-5 mr-2 text-indigo-500" /> Filter Options
            </h2>
          </div>
          
          <div className="space-y-4">
            {/* Project Selector */}
            <div className="relative">
              <label htmlFor="project-select" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Select Project
              </label>
              <select
                id="project-select"
                value={selectedProject}
                onChange={(e) => setSelectedProject(e.target.value)}
                className="w-full pl-3 pr-10 py-2 text-base border-gray-300 dark:border-slate-600 bg-white dark:bg-slate-900 dark:text-gray-100 focus:outline-none focus:ring-blue-500 focus:border-blue-500 rounded-lg shadow-sm appearance-none border"
              >
                {projects.map((proj) => (
                  <option key={proj} value={proj}>{proj}</option>
                ))}
              </select>
              <ChevronDownIcon className="absolute right-3 top-[34px] w-4 h-4 text-gray-400 dark:text-gray-400 pointer-events-none" />
            </div>

            {/* General Filters */}
            {filters.map((filter) => (
              <div key={filter.label}>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  {filter.label}
                </label>
                <div className="p-2 border border-gray-300 dark:border-slate-600 rounded-lg text-sm text-gray-600 dark:text-gray-300 bg-gray-50 dark:bg-slate-900">
                  {filter.default}
                </div>
              </div>
            ))}
          </div>
        </aside>

        {/* Right Column (Report/Chart Visualization) - Takes 3/4 width */}
        <div className="lg:col-span-3">
          <div className="bg-white dark:bg-slate-800 p-6 rounded-xl shadow-lg border border-gray-100 dark:border-slate-700">
            
            {/* View Mode Toggle */}
            <div className="flex justify-between items-center border-b pb-4 mb-4">
              <h2 className="text-xl font-semibold text-gray-700 dark:text-gray-200">
                Evaluation Visualization: {selectedProject}
              </h2>
              <div className="flex space-x-2 p-1 bg-gray-100 dark:bg-slate-700/50 rounded-lg">
                <button
                  onClick={() => setViewMode('chart')}
                  className={`p-2 rounded-lg transition-colors flex items-center text-sm font-medium ${
                    viewMode === 'chart' ? 'bg-blue-600 text-white shadow' : 'text-gray-600 hover:bg-gray-200'
                  }`}
                  aria-pressed={viewMode === 'chart'}
                >
                  <BarChart2Icon className="w-5 h-5 mr-1" /> Chart View
                </button>
                <button
                  onClick={() => setViewMode('table')}
                  className={`p-2 rounded-lg transition-colors flex items-center text-sm font-medium ${
                    viewMode === 'table' ? 'bg-blue-600 text-white shadow' : 'text-gray-600 hover:bg-gray-200'
                  }`}
                  aria-pressed={viewMode === 'table'}
                >
                  <TableIcon className="w-5 h-5 mr-1" /> Data Table
                </button>
              </div>
            </div>

            {/* Visualization Content */}
            <div className="min-h-[400px] flex items-center justify-center bg-gray-50 dark:bg-slate-900 rounded-lg border border-dashed border-gray-200 dark:border-slate-700">
              {viewMode === 'chart' ? (
                <div className="text-center text-gray-500 dark:text-gray-300 p-8">
                  <BarChart2Icon className="w-10 h-10 mx-auto mb-3 text-blue-400 dark:text-blue-300" />
                  <p>Placeholder for Interactive Evaluation Chart (e.g., performance over time).</p>
                </div>
              ) : (
                <div className="text-center text-gray-500 dark:text-gray-300 p-8">
                  <TableIcon className="w-10 h-10 mx-auto mb-3 text-blue-400 dark:text-blue-300" />
                  <p>Placeholder for Detailed Evaluation Data Table (scrollable rows).</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
      
    </div>
  );
}