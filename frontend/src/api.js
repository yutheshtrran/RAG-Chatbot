import axios from "axios";

// Backend base URL - adjust if running on different host/port
const API_BASE_URL = "http://127.0.0.1:5000/api";

/**
 * Send message to the patient-specific chatbot.
 * Works with or without explicit patient ID in the message.
 * 
 * @param {string} userInput - Natural language input or patient ID + question
 * @param {string|null} patientId - Optional explicit patient ID
 * @returns {Promise<string>} reply from chatbot
 */
export async function sendMessage(userInput, patientId = null) {
  if (!userInput || !userInput.trim()) {
    return "⚠️ Please provide a question.";
  }

  // If patient ID is provided explicitly, use it
  let finalPatientId = patientId;
  let message = userInput;

  // If no explicit patient ID, try to extract from message
  if (!finalPatientId) {
    const match = userInput.match(/patient\s+(?:ID\s+)?(\d+)/i);
    if (match) {
      finalPatientId = match[1];
      message = userInput.replace(match[0], "").trim() || "Show me the patient history";
    }
  }

  if (!finalPatientId) {
    return "⚠️ Please provide a patient ID (e.g., 'patient 001 what is their diagnosis')";
  }

  try {
    const response = await axios.post(`${API_BASE_URL}/chat`, {
      patient_id: finalPatientId,
      message: message
    });

    return response.data.reply || "⚠️ No reply received.";
  } catch (error) {
    console.error("API Error:", error);
    
    if (error.response) {
      return `⚠️ Backend error: ${error.response.data?.error || "Unknown error"}`;
    } else if (error.request) {
      return "⚠️ Could not connect to backend. Make sure the server is running on http://127.0.0.1:5000";
    } else {
      return `⚠️ Error: ${error.message}`;
    }
  }
}

/**
 * Upload patient files to the backend.
 * 
 * @param {string} patientId - Patient ID
 * @param {string} name - Patient name (optional)
 * @param {number} age - Patient age (optional)
 * @param {string} gender - Patient gender (optional)
 * @param {FileList} files - Files to upload
 * @returns {Promise<object>} Upload response
 */
export async function uploadPatientFiles(patientId, name = "", age = "", gender = "", files = []) {
  if (!patientId) {
    return { error: "Patient ID is required" };
  }

  if (!files || files.length === 0) {
    return { error: "No files selected" };
  }

  const formData = new FormData();
  formData.append("patient_id", patientId);
  
  if (name) formData.append("name", name);
  if (age) formData.append("age", age);
  if (gender) formData.append("gender", gender);

  for (let file of files) {
    formData.append("files", file);
  }

  try {
    const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
      headers: {
        "Content-Type": "multipart/form-data"
      }
    });

    return response.data;
  } catch (error) {
    console.error("Upload Error:", error);
    
    if (error.response) {
      return { error: error.response.data?.error || "Upload failed" };
    } else if (error.request) {
      return { error: "Could not connect to backend" };
    } else {
      return { error: error.message };
    }
  }
}

