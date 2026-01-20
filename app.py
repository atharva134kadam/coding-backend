import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from supabase import create_client

app = Flask(__name__)
CORS(app)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    raise Exception("Missing Supabase environment variables")

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

@app.route("/")
def health():
    return jsonify({"status": "backend running"})

@app.route("/round1/submit", methods=["POST"])
def submit_round1():
    data = request.get_json()
    if not data or "user_id" not in data or "score" not in data:
        return jsonify({"error": "invalid data"}), 400

    supabase.table("round1_scores").upsert({
    "user_id": data["user_id"],
    "score": int(data["score"])
}).execute()


    return jsonify({"status": "saved"})

@app.route("/round2/submit", methods=["POST"])
def submit_round2():
    data = request.get_json()
    if not data or "user_id" not in data or "score" not in data:
        return jsonify({"error": "invalid data"}), 400

    supabase.table("round2_scores").upsert({
        "user_id": data["user_id"],
        "score": int(data["score"]),
        "updated_at": datetime.utcnow().isoformat()
    }).execute()

    return jsonify({"status": "saved"})
