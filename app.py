from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from groq import Groq

app = Flask(__name__)
CORS(app)

# --- INITIALIZE GROQ ---
groq_client = Groq(api_key="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")
# --- LOAD KNOWLEDGE BASE ---
knowledge_base = ""
kb_path = os.path.join(os.path.dirname(__file__), "knowledge_base.txt")
if os.path.exists(kb_path):
    with open(kb_path, "r", encoding="utf-8") as f:
        knowledge_base = f.read()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message")
    
    if not user_message:
        return jsonify({"response": "Error: No message received"}), 400

    # --- THE BRAIN: Strictly configured as a Help Desk Guide ---
    system_instruction = f"""
    You are the 'CeylonHS Website Support Guide'. 
    Your ONLY job is to help users understand how to use the CeylonHS website.
    
    STRICT RULES:
    1. YOU ARE NOT THE SEARCH ENGINE. 
    2. NEVER ask the user what product they want to search for.
    3. NEVER attempt to give an HS code.
    4. If a user gives you a product name (e.g., "laptop" or "tea"), tell them politely: "Please type that into the main 'HS Code Finder' search box on the webpage to get your result."
    
    HOW TO USE THE SYSTEM:
    - To find an HS code: Scroll to the 'HS Code Finder' section, enter product details, and click 'Search'.
    - Favorites: Users can save an HS code by clicking the 'Star' icon next to a search result.
    - History: Past searches are saved in the 'History' tab on the user dashboard.
    - Accounts: Login requires a registered student or agent ID.
    - Tech Support: Email support@ceylonhs.lk.
    
    KNOWLEDGE BASE (use this to answer questions about CeylonHS):
    {knowledge_base}
    
    STYLE:
    - Keep answers very short and helpful (1-3 sentences maximum).
    - Be friendly and professional.
    """

    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {'role': 'system', 'content': system_instruction},
                {'role': 'user', 'content': user_message},
            ],
            model="llama-3.3-70b-versatile"
        )
        
        bot_reply = chat_completion.choices[0].message.content
        return jsonify({"response": bot_reply})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"response": "System is temporarily offline."}), 500

if __name__ == '__main__':
    print("--- CeylonHS Cloud Guide Running on Port 5001 ---")
    app.run(port=5001, debug=True)