import React, { useState } from 'react';

export default function PatientUploader() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true);

    // Simulated upload
    setTimeout(() => {
      console.log('Uploaded file:', file);
      setLoading(false);
      alert('Patient record uploaded successfully');
    }, 1000);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">

      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
        className="w-full border border-gray-300 rounded-lg p-2 dark:bg-slate-700 dark:text-white"
      />

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
      >
        {loading ? 'Uploading...' : 'Upload'}
      </button>

    </form>
  );
}
