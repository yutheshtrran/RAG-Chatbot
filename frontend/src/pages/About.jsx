import React from 'react';
// Assuming Icons.jsx includes relevant icons like Info, EvaluationIcon, UserIcon, and now a HeartIcon or similar
import { InfoIcon, EvaluationIcon, UserIcon, HeartHandshakeIcon, ShieldIcon, ActivityIcon } from '../components/Icons'; 
// Assuming ShieldIcon and ActivityIcon (or similar) are available in your Icons.jsx

export default function About() {
  return (
    // Base container is slightly elevated from the background
    <div className="p-4 sm:p-8 lg:p-10 max-w-6xl mx-auto bg-white dark:bg-slate-800 rounded-xl shadow-2xl mt-8 mb-12 border border-gray-100 dark:border-slate-700">
      
      {/* Header Section */}
      <header className="text-center mb-12 pb-6 border-b border-gray-100 dark:border-slate-700">
        <h1 className="text-4xl sm:text-5xl font-extrabold text-gray-900 dark:text-white tracking-tight">
          About <span className="text-blue-600 dark:text-blue-400">MediRAG</span>
        </h1>
        <p className="mt-4 text-xl text-gray-500 dark:text-gray-300 max-w-3xl mx-auto">
          Your intelligent partner for clinical data evaluation and RAG system interaction.
        </p>
      </header>

      {/* Mission & Technology Section (2-column Grid) */}
      <section className="grid md:grid-cols-2 gap-8 mb-16">
        {/* Mission Card */}
        <div className="p-8 bg-gray-50 dark:bg-slate-900 rounded-xl border border-gray-100 dark:border-slate-700 shadow-sm transition hover:shadow-md">
          <div className="flex items-center text-blue-600 mb-4">
            <EvaluationIcon className="w-8 h-8 mr-3" />
            <h3 className="text-2xl font-bold text-gray-900 dark:text-white">Our Mission</h3>
          </div>
          <p className="text-gray-700 dark:text-gray-300 leading-relaxed text-lg">
            To enhance the precision and accessibility of medical data analysis by leveraging **Retrieval-Augmented Generation (RAG)** technology. We aim to provide clear, context-aware evaluations, streamlining decision-making for healthcare professionals and researchers.
          </p>
        </div>
        
        {/* Technology Card */}
        <div className="p-8 bg-gray-50 dark:bg-slate-900 rounded-xl border border-gray-100 dark:border-slate-700 shadow-sm transition hover:shadow-md">
          <div className="flex items-center text-indigo-600 mb-4">
            <ActivityIcon className="w-8 h-8 mr-3" />
            <h3 className="text-2xl font-bold text-gray-900 dark:text-white">Our Technology</h3>
          </div>
          <p className="text-gray-700 dark:text-gray-300 leading-relaxed text-lg">
            MediRAG is built on a custom RAG pipeline integrated with clinical databases. This allows the AI to ground its conversational responses and evaluations in reliable, up-to-date domain-specific knowledge, ensuring high factual accuracy and compliance.
          </p>
        </div>
      </section>

      {/* Key Features Section (Completed with three features) */}
      <section className="mb-16">
        <h2 className="text-3xl font-bold text-gray-800 dark:text-gray-100 mb-8 border-b-2 border-blue-100 pb-3">Why Choose MediRAG?</h2>
        <div className="space-y-6">
          
          {/* Feature 1: Contextual Accuracy (Completed) */}
          <div className="flex items-start p-5 bg-white dark:bg-slate-800 border border-l-4 border-l-blue-500 rounded-xl shadow-md transition hover:shadow-lg">
            <div className="flex-shrink-0 text-blue-500 mt-1">
              <ShieldIcon className="w-6 h-6" /> 
            </div>
            <div className="ml-4">
              <h4 className="font-semibold text-lg text-gray-900 dark:text-white">Contextual Accuracy</h4>
              <p className="text-gray-600 dark:text-gray-300">Responses are dynamically generated from a proprietary medical knowledge base, minimizing hallucinations and maximizing reliability.</p>
            </div>
          </div>
          
          {/* Feature 2: Compliance & Security (Completed and Enhanced) */}
          <div className="flex items-start p-5 bg-white dark:bg-slate-800 border border-l-4 border-l-indigo-500 rounded-xl shadow-md transition hover:shadow-lg">
            <div className="flex-shrink-0 text-indigo-500 mt-1">
              <HeartHandshakeIcon className="w-6 h-6" />
            </div>
            <div className="ml-4">
              <h4 className="font-semibold text-lg text-gray-900 dark:text-white">Dedicated Clinical Focus</h4>
              <p className="text-gray-600 dark:text-gray-300">Unlike general models, MediRAG is fine-tuned exclusively for medical terminology and evaluation criteria, ensuring domain-specific excellence.</p>
            </div>
          </div>

          {/* Feature 3: Live Performance Monitoring (New Feature) */}
          <div className="flex items-start p-5 bg-white dark:bg-slate-800 border border-l-4 border-l-green-500 rounded-xl shadow-md transition hover:shadow-lg">
            <div className="flex-shrink-0 text-green-500 mt-1">
              <EvaluationIcon className="w-6 h-6" />
            </div>
            <div className="ml-4">
              <h4 className="font-semibold text-lg text-gray-900 dark:text-white">Performance Transparency</h4>
              <p className="text-gray-600 dark:text-gray-300">Access real-time RAG performance metrics on the Evaluation page, giving you full confidence in the system's accuracy.</p>
            </div>
          </div>
          
        </div>
      </section>

      {/* Footer/Call-to-Action Section */}
      <section className="text-center p-8 bg-blue-50 dark:bg-slate-900/40 rounded-xl border border-blue-200 dark:border-slate-700">
        <h3 className="text-2xl font-bold text-blue-800 mb-3">Ready to Start Evaluating?</h3>
        <p className="text-blue-700 dark:text-blue-200 mb-6 max-w-xl mx-auto">
          Jump into the dashboard to interact with the AI assistant or navigate to the evaluation reports.
        </p>
        <a 
          href="/dashboard" 
          className="inline-flex items-center px-8 py-3 border border-transparent text-base font-semibold rounded-full shadow-lg text-white bg-blue-600 hover:bg-blue-700 dark:bg-blue-600 dark:hover:bg-blue-700 transition duration-150 transform hover:scale-105"
        >
          Go to Dashboard
          <InfoIcon className="w-5 h-5 ml-2" />
        </a>
      </section>
    </div>
  );
}