import axios from "axios";

// Backend base URL
const API_URL = "http://127.0.0.1:5000/api/chat";

/**
 * Extract patient ID from natural language input.
 * @param {string} userInput
 * @returns {object} { patientId, message }
 */
function extractPatientIdAndMessage(userInput) {
  const match = userInput.match(/patient(?: ID)? (\d+)/i);
  if (match) {
    const patientId = match[1];
    const message = userInput.replace(match[0], "").trim() || "Show me the patient history";
    return { patientId, message };
  }
  return { patientId: null, message: userInput };
}

/**
 * Send message to the patient-specific chatbot.
 * @param {string} userInput - Natural language input
 * @returns {string} reply from chatbot
 */
export async function sendMessage(userInput) {
  const { patientId, message } = extractPatientIdAndMessage(userInput);

  if (!patientId || !message) {
    return "⚠️ Please provide a valid patient ID and a message.";
  }

  try {
    const response = await axios.post(API_URL, { patient_id: patientId, message });
    return response.data.reply || "⚠️ No reply received.";
  } catch (error) {
    console.error("API Error:", error);
    return "⚠️ Error: Could not connect to the backend.";
  }
}
