from flask import Flask, request, jsonify, render_template_string
import random

app = Flask(__name__)

@app.route("/")
def home():
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Nexa Chatbot 🤖</title>
<style>
body { font-family: 'Segoe UI', sans-serif; background: linear-gradient(135deg, #1a237e, #3949ab); display:flex; justify-content:center; align-items:center; height:100vh; margin:0; }
.chat-container { width:400px; height:550px; background: rgba(255,255,255,0.1); backdrop-filter: blur(15px); border-radius:25px; display:flex; flex-direction:column; box-shadow:0 8px 40px rgba(0,0,0,0.5); overflow:hidden; border:1px solid rgba(255,255,255,0.2);}
.chat-header { background: linear-gradient(90deg, #1a237e, #3949ab); color:#fff; padding:20px; font-size:22px; text-align:center; font-weight:bold; letter-spacing:1px; text-shadow:0 2px 5px rgba(0,0,0,0.2);}
.chat-box { flex:1; padding:20px; overflow-y:auto; display:flex; flex-direction:column; gap:10px;}
.message { padding:14px 20px; border-radius:20px; max-width:70%; word-wrap:break-word; opacity:0; transform:translateY(20px); animation:slideIn 0.4s forwards; position:relative; }
@keyframes slideIn { to {opacity:1; transform:translateY(0);} }
.user { background: linear-gradient(145deg,#283593,#1a237e); color:#fff; align-self:flex-end; border-bottom-right-radius:5px; }
.bot { background: rgba(255,255,255,0.3); color:#fff; align-self:flex-start; border-bottom-left-radius:5px; backdrop-filter: blur(10px); border:1px solid rgba(255,255,255,0.2); }
.typing { display:flex; gap:5px; }
.typing span { width:6px; height:6px; background:#1a237e; border-radius:50%; animation:blink 1.4s infinite both;}
.typing span:nth-child(1){animation-delay:0s;} .typing span:nth-child(2){animation-delay:0.2s;} .typing span:nth-child(3){animation-delay:0.4s;}
@keyframes blink { 0%,80%,100% {transform:scale(0);opacity:0.3;} 40% {transform:scale(1);opacity:1;} }
.chat-input { display:flex; padding:15px; background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); border-top:1px solid rgba(255,255,255,0.2);}
.chat-input input { flex:1; padding:14px 20px; border-radius:25px; border:1px solid rgba(255,255,255,0.3); outline:none; font-size:16px; color:#fff; background:rgba(0,0,0,0.2); margin-right:10px; backdrop-filter: blur(5px);}
.chat-input input::placeholder { color: rgba(255,255,255,0.7);}
.chat-input button { background: linear-gradient(145deg, #1a237e, #3949ab); color:white; border:none; border-radius:50%; width:50px; height:50px; cursor:pointer; font-size:20px; display:flex; justify-content:center; align-items:center; transition: transform 0.2s, background 0.3s; }
.chat-input button:hover { transform: scale(1.1); background: linear-gradient(145deg, #283593, #1a237e); }
.chat-box::-webkit-scrollbar { width:5px; } .chat-box::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.3); border-radius:5px; }
</style>
</head>
<body>
<div class="chat-container">
<div class="chat-header">Nexa 🤖</div>
<div id="chatbox" class="chat-box"></div>
<form class="chat-input">
<input type="text" id="userInput" placeholder="Type a message..." required />
<button type="submit">➤</button>
</form>
</div>

<script>
const chatBox = document.getElementById("chatbox");
const input = document.getElementById("userInput");

document.querySelector("form").addEventListener("submit", async function(e){
    e.preventDefault();
    const message = input.value.trim();
    if(!message) return;

    // 1️⃣ Show user message immediately
    const userMsg = document.createElement("div");
    userMsg.className = "message user";
    userMsg.textContent = message;
    chatBox.appendChild(userMsg);
    chatBox.scrollTop = chatBox.scrollHeight;

    input.value = "";

    // 2️⃣ Add bot typing indicator
    const botMsg = document.createElement("div");
    botMsg.className = "message bot";
    botMsg.innerHTML = `<div class="typing"><span></span><span></span><span></span></div>`;
    chatBox.appendChild(botMsg);
    chatBox.scrollTop = chatBox.scrollHeight;

    // 3️⃣ Call backend for reply
    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {"Content-Type":"application/json"},
            body: JSON.stringify({message})
        });
        const data = await response.json();
        // Remove typing and show reply
        botMsg.innerHTML = data.reply;
        chatBox.scrollTop = chatBox.scrollHeight;
    } catch(err) {
        botMsg.innerHTML = "Error: Could not get reply.";
    }
});
</script>
</body>
</html>
    """)

# Backend: simple predefined replies
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message","").lower()
    if "hello" in user_message or "hi" in user_message:
        reply = "Hello! How can I help you today?😊"
    elif "how are you" in user_message:
        reply = "I'm doing great 😃 Thanks for asking!"
    elif "bye" in user_message:
        reply = "Goodbye! Have a great day 👋"
    elif "help" in user_message:
        reply = "Sure! What do you need help with?😊"
    elif "your name" in user_message:
        reply = "I'm Nexa, your friendly chatbot 🤖"
    elif "what can you do" in user_message:
        reply = "I can chat with you and assist with simple tasks!😉☺️"
    elif "joke" in user_message:
        jokes = [
            "Why don't scientists trust atoms😉? Because they make up everything🤷‍♀️🤷‍♀️!",
            "Why did the scarecrow win an award🤔🤔? Because he was outstanding in his field🤣🤣!",
            "Why don't programmers like nature😎😎? It has too many bugs😁😁😆."
        ]
        reply = random.choice(jokes)
    elif "weather" in user_message:
        reply = "I can't check the weather yet, but I hope it's nice where you are💕🥰!"
    elif "time" in user_message:
        from datetime import datetime
        now = datetime.now().strftime("%H:%M")
        reply = f"The current time is {now}."
    elif "who created you" in user_message or "who made you" in user_message:
        reply = "I was created by a talented developer..Siri❤️!"
    elif "thank you" in user_message or "thanks" in user_message:
        reply = "You're welcome! 😊"
    elif "love" in user_message:
        reply = "Love is a beautiful thing! ❤️"
    else:
        generic_replies = [
            "Interesting! Tell me more.",
            "Hmm, I need to think about that...",
            "Sorry, I don't understand that yet."
        ]
        reply = random.choice(generic_replies)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
