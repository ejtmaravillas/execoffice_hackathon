from flask import Flask, request, jsonify
from flask_cors import CORS
import pdfplumber
from sentence_transformers import SentenceTransformer, util

app = Flask(__name__)
CORS(app)

# Load the SentenceTransformer model
summarization_model = SentenceTransformer('all-MiniLM-L6-v2')

# Summarization logic
def summarize_text(sentences, summarization_model):
    try:
        if len(sentences) < 3:
            # If there are less than 3 sentences, return them as-is
            return " ".join(sentences)

        # Generate embeddings for all sentences
        embeddings = summarization_model.encode(sentences, convert_to_tensor=True)

        # Perform semantic search (find the top 3 most relevant sentences)
        search_results = util.semantic_search(embeddings, embeddings, top_k=3)

        # Extract the top 3 sentences (avoid unpacking issues)
        top_indices = [result['corpus_id'] for result in search_results[0]]
        summary = " ".join([sentences[i] for i in top_indices])

        return summary
    except Exception as e:
        print(f"Summarization error: {e}")
        return "Error during summarization."

@app.route('/extract-and-summarize-pdf', methods=['POST'])
def extract_and_summarize_pdf():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided."}), 400

        file = request.files['file']
        pdf_text = ""

        # Extract text from PDF
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                extracted_text = page.extract_text()
                if extracted_text:
                    pdf_text += extracted_text + "\n"

        if not pdf_text.strip():
            return jsonify({"error": "No extractable text found in the PDF."}), 400

        # Split the text into sentences
        sentences = [s.strip() for s in pdf_text.split("\n") if s.strip()]

        # Summarize the extracted text
        summary = summarize_text(sentences, summarization_model)

        return jsonify({"text": pdf_text, "summary": summary})

    except Exception as e:
        print(f"Error: {e}")  # Log the error in the console
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
