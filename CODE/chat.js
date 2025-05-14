window.sendMessage = async function () {
  const userMessage = input.value.trim();
  if (!userMessage) return;

  appendMessage("user", userMessage);
  input.value = "";

  const typingDiv = document.createElement("div");
  typingDiv.classList.add("bot-message");
  typingDiv.textContent = "Typing...";
  chatMessages.appendChild(typingDiv);

  try {
    const response = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: userMessage }),
    });

    const data = await response.json();
    console.log("Bot response data:", data);
    chatMessages.removeChild(typingDiv);
    appendMessage("bot", data.response);  // ✅ FIXED LINE
  } catch (error) {
    console.error("Error sending message:", error);
    chatMessages.removeChild(typingDiv);
    appendMessage("bot", "⚠️ Error: Could not connect to backend.");
  }
};
