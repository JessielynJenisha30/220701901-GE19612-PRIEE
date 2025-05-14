from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import subprocess

app = FastAPI()

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gen Z system prompt
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

❌ Never explain anything like a narrator or give summaries of the conversation. Never include any explanation like “This chat is designed to…” or “This shows how…” — just reply like a human bestie. No quizzes, no teaching, no AI disclaimers. Just real convos, always.

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
"""

# Conversation history
chat_history = [{"role": "system", "content": system_prompt}]

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("message", "")

    print(f"📝 User: {user_input}")

    chat_history.append({"role": "user", "content": user_input})

    # Build prompt
    prompt_text = "\n".join([
        f"{msg['role'].capitalize()}: {msg['content']}" if msg['role'] != "system" else msg['content']
        for msg in chat_history
    ])

    try:
        print("📤 Sending prompt to Ollama...")
        print(f"📄 Prompt:\n{prompt_text}\n")

        result = subprocess.run(
            ["ollama", "run", "phi"],
            input=prompt_text.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60
        )

        raw_response = result.stdout.decode("utf-8").strip()
        error = result.stderr.decode("utf-8").strip()

        print(f"📥 Raw Response: {raw_response}")
        if error:
            print(f"⚠️ STDERR: {error}")

        # Fallback if model is empty
        if not raw_response:
            clean_response = "🥲 Oops, I zoned out. Can you say that again?"
        else:
            # Remove unwanted prefixes
            clean_response = raw_response
            if "Model response:" in clean_response:
                clean_response = clean_response.split("Model response:")[-1].strip()
            if clean_response.startswith("AI:"):
                clean_response = clean_response[3:].strip()

        chat_history.append({"role": "assistant", "content": clean_response})
        return {"response": clean_response}

    except Exception as e:
        print(f"❌ Exception: {e}")
        return {"response": "⚠️ Error: Something went wrong on the server side."}
