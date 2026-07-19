from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Load model (or fallback)
try:
    legal_ai = pipeline("text-generation", model="./models/legal_ai")
except:
    print("⚠️ Using fallback model.")
    legal_ai = pipeline("text-generation", model="gpt2")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "No text provided"}), 400

    prompt = f"""
Explain this legal text in plain, simple English. 
No jargon. Short sentences. Say what it actually means.

Text:
{text}

Plain English explanation:
"""
    result = legal_ai(prompt, max_new_tokens=150, do_sample=True, temperature=0.7)
    raw = result[0]["generated_text"]
    clean = raw.replace(prompt, "").strip()
    return jsonify({"analysis": clean or "Could not generate explanation."})

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.json
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "No text provided"}), 400

    prompt = f"""
Summarize this legal text in one or two simple sentences:

{text}

Summary:
"""
    result = legal_ai(prompt, max_new_tokens=80, do_sample=True, temperature=0.7)
    raw = result[0]["generated_text"]
    clean = raw.replace(prompt, "").strip()
    return jsonify({"summary": clean or "Could not generate summary."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
