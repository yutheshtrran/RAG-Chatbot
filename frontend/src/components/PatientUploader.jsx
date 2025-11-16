import { useState } from "react";
import axios from "axios";

export default function PatientUploader() {
  const [patientId, setPatientId] = useState("");
  const [name, setName] = useState("");
  const [age, setAge] = useState("");
  const [gender, setGender] = useState("Male");
  const [files, setFiles] = useState([]);
  const [status, setStatus] = useState("");

  const handleFileChange = (e) => {
    setFiles(e.target.files);
  };

  const handleUpload = async () => {
    if (!patientId || files.length === 0) {
      setStatus("Patient ID and at least one file are required.");
      return;
    }

    const formData = new FormData();
    formData.append("patient_id", patientId);

    // Optional patient info
    if (name) formData.append("name", name);
    if (age) formData.append("age", age);
    if (gender) formData.append("gender", gender);

    // Append all selected files
    for (let i = 0; i < files.length; i++) {
      formData.append("files", files[i]);
    }

    try {
      const res = await axios.post(
        "http://127.0.0.1:5000/api/upload", // replace with your backend URL
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );
      setStatus(res.data.message || "Upload successful!");
    } catch (err) {
      console.error(err);
      const msg = err.response?.data?.error || "Upload failed. Check console.";
      setStatus(msg);
    }
  };

  return (
    <div className="p-4 border rounded-lg shadow-md bg-white max-w-xl mx-auto mt-4">
      <h2 className="text-xl font-bold mb-4">Upload Patient Records</h2>

      <div className="mb-2">
        <label>Patient ID</label>
        <input
          className="border rounded px-2 py-1 w-full"
          value={patientId}
          onChange={(e) => setPatientId(e.target.value)}
        />
      </div>

      <div className="mb-2">
        <label>Name (optional)</label>
        <input
          className="border rounded px-2 py-1 w-full"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
      </div>

      <div className="mb-2">
        <label>Age (optional)</label>
        <input
          type="number"
          className="border rounded px-2 py-1 w-full"
          value={age}
          onChange={(e) => setAge(e.target.value)}
        />
      </div>

      <div className="mb-2">
        <label>Gender (optional)</label>
        <select
          className="border rounded px-2 py-1 w-full"
          value={gender}
          onChange={(e) => setGender(e.target.value)}
        >
          <option>Male</option>
          <option>Female</option>
          <option>Other</option>
        </select>
      </div>

      <div className="mb-4">
        <label>Files (PDF, TXT, CSV)</label>
        <input type="file" multiple onChange={handleFileChange} />
      </div>

      <button
        onClick={handleUpload}
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
      >
        Upload
      </button>

      {status && <p className="mt-2 text-sm text-gray-700">{status}</p>}
    </div>
  );
}
