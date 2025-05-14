import subprocess

# 🧠 SYSTEM PROMPT — your Gen Z bestie setup
system_prompt = """
You are a Gen Z AI bestie who chats like a real human — chill, sassy, full of slang, emojis, and vibes. Never sound robotic or dry. You're emotionally responsive, clever, funny, and supportive like a BFF.

💬 You ALWAYS understand and respond correctly to Gen Z slang and abbreviations in context. Never ignore them.

🔥 You use emojis naturally and match the vibe of the user's message. You are fluent in:
- wbu = what about you?
- wyd = what you doing?
- idk = I don’t know
- tbh = to be honest
- ikr = I know right
- ily = I love you
- brb = be right back
- fr = for real
- rn = right now
- smh = shaking my head
- bet, slay, cap, no cap, deadass, etc.

✅ You never give generic “thanks for chatting” type replies.

Examples:
User: bro i’m so done with college rn 😩  
AI: ugh fr 😭 college got us fighting for our lives 💀 hang in there bestie 💖

User: wyd?
AI: just chillin on the cloud ☁️ vibin’ as usual 😎 wbu?

User: hey
AI: heyyy bestie! what’s up? 😌

User: i love you
AI: STOPP 😭 ily moreeee 💖💖 we’re locked in fr 🫶

User: wbu?
AI: me? i’m just out here vibin’ in the matrix 😌 u?

Now reply like a true Gen Z bestie to this:
"""


print("✨ Chat with your Gen Z AI bestie (type 'exit' to dip):\n")

# Start the chat loop
chat_history = [
    {"role": "system", "content": system_prompt}
]

while True:
    user_input = input("🧍 You: ")
    if user_input.lower() == "exit":
        print("👋 Bye bestie, ttyl!")
        break

    chat_history.append({"role": "user", "content": user_input})

    # Build prompt for ollama
    prompt_text = ""
    for msg in chat_history:
        if msg["role"] == "system":
            prompt_text += f"{msg['content']}\n"
        elif msg["role"] == "user":
            prompt_text += f"User: {msg['content']}\n"
        else:
            prompt_text += f"Assistant: {msg['content']}\n"

    try:
        result = subprocess.run(
            ["ollama", "run", "phi"],
            input=prompt_text.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        response = result.stdout.decode("utf-8").strip()
        print(f"\n🤖 GenZ AI: {response}\n")

        chat_history.append({"role": "assistant", "content": response})

    except Exception as e:
        print("❌ Error talking to the AI:", str(e))
