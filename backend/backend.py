import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename


from model import ChatBotModel
from utils import extract_text_from_pdf, save_resume_to_csv


app = Flask(__name__)


UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
models = {}




@app.route("/upload_resume", methods=["POST"])
def upload_resume():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.endswith(".pdf"):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)
        resume_text = extract_text_from_pdf(file_path)
        file_id = os.path.splitext(filename)[0]
        save_resume_to_csv(file_id, resume_text)
        models[file_id] = ChatBotModel(resume_text)

        return jsonify({"message": "Resume uploaded and processed successfully!", "file_id": file_id})
    else:
        return jsonify({"error": "Invalid file format. Only PDF is allowed."}), 400


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "question" not in data or "file_id" not in data:
        return jsonify({"error": "Invalid input. Provide 'question' and 'file_id'."}), 400
    
    question = data["question"]
    file_id = data["file_id"]

    if file_id not in models:
        return jsonify({"error": "Invalid File_id'."}), 400

    model = models[file_id]
    answer = model.generate_response(question)

    return jsonify({"answer": answer})


if __name__ == "__main__":
    app.run(debug=True)
