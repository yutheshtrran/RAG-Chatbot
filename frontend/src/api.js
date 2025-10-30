import axios from "axios";

// Use your backend IP and port
const API_URL = "http://172.20.10.2:5000/api/chat";

export async function sendMessage(message) {
  try {
    const response = await axios.post(API_URL, { message });
    
    // Your backend now returns { reply: { reply: "...text..." } }
    // So extract nested reply
    return response.data.reply?.reply || "⚠️ No reply received.";
  } catch (error) {
    console.error("API Error:", error);
    return "⚠️ Error: Could not connect to the backend.";
  }
}
