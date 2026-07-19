from flask import Flask, request, jsonify
from transformers import pipeline
import os

app = Flask(__name__)

# ---------- LOAD MODEL ----------
model_path = "./models/legal_ai"

if os.path.exists(model_path):
    legal_ai = pipeline("text-generation", model=model_path)
else:
    print("⚠️ No trained model found. Using fallback.")
    legal_ai = pipeline("text-generation", model="gpt2")

# ---------- ROUTES ----------

@app.route("/", methods=["GET"])
def home():
    return {"message": "Legal AI API is running."}

@app.route("/ping", methods=["GET"])
def ping():
    return {"status": "alive"}

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Short, direct prompt
    prompt = f"Risks in this clause:\n{text}\nRisks:"
    try:
        result = legal_ai(prompt, max_new_tokens=100, do_sample=True, temperature=0.7)
        raw = result[0]["generated_text"]
        # Remove the prompt from the response
        clean = raw.replace(prompt, "").strip()
        return jsonify({"analysis": clean or "No specific risks found."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.json
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "No text provided"}), 400

    prompt = f"Summary:\n{text}\nSummary:"
    try:
        result = legal_ai(prompt, max_new_tokens=80, do_sample=True, temperature=0.7)
        raw = result[0]["generated_text"]
        clean = raw.replace(prompt, "").strip()
        return jsonify({"summary": clean or "No summary available."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------- RUN ----------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)