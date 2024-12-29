# AI-Powered Interview Assistant

An interactive application that allows users to upload their resumes, process them for content extraction, and simulate interview Q&A sessions with an AI-powered chatbot.

## Features

- **Resume Upload:** Upload resumes in PDF format.
- **Content Extraction:** Extract and store resume content for analysis.
- **AI Chatbot:** Ask interview-style questions based on the resume content.
- **Interactive UI:** Streamlit-based frontend for seamless user experience.

---

## Backend

### Tech Stack

- **Flask:** Backend framework for REST API.
- **PyPDF2:** Extract text from PDF resumes.
- **Google Generative AI:** Chatbot model powered by generative AI.
- **CSV Storage:** Store extracted resume content for reference.

### Endpoints

1. **Upload Resume**
   - URL: `/upload_resume`
   - Method: `POST`
   - Content-Type: `multipart/form-data`
   - Request: `file` (PDF file)
   - Response: JSON with a success message and `file_id`.

2. **Chat**
   - URL: `/chat`
   - Method: `POST`
   - Content-Type: `application/json`
   - Request:
     ```json
     {
       "question": "What are your skills?",
       "file_id": "example_resume"
     }
     ```
   - Response: JSON with the chatbot's answer.

---

## Frontend

### Tech Stack

- **Streamlit:** Web interface for user interaction.
- **Requests:** Communication with the backend.

### Features

- **Upload Section:** Upload resumes for processing.
- **Chat Interface:** Interactive Q&A section for simulated interviews.
- **Dynamic Chat Rendering:** Displays user and bot messages with styled chat bubbles.

### UI Components

- **Resume Upload:** Drag and drop PDF files for upload.
- **Interactive Chat:** Input questions and view bot responses dynamically.

---

## Installation and Setup

### Prerequisites

- Python 3.8 or above
- Flask
- Streamlit
- Required Python Libraries: `requirements.txt`

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
