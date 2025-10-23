const BASE_URL = "http://127.0.0.1:5000/api";

export async function sendMessageToBackend(message) {
  try {
    const response = await fetch(`${BASE_URL}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });

    if (!response.ok) throw new Error(`Error ${response.status}`);

    const data = await response.json();
    return data; // expects { reply: "..." }
  } catch (err) {
    console.error("Backend error:", err);
    return { reply: "Sorry, something went wrong!" };
  }
}
