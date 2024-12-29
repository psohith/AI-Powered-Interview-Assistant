import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()


class ChatBotModel:
    def __init__(self, resume_content):
        self.model = genai.GenerativeModel("models/gemini-2.0-flash-exp")
        self.resume_content = resume_content
        self.chat_history = []

    def _generate_response(self, prompt):
        return self.model.generate_content(prompt).text.strip()

    def _contextualize_question(self, question):
        """
        Reformulate the question based on chat history to make it standalone.
        """
        context_prompt = (
            "Given a chat history and the latest user question "
            "which might reference context in the chat history, "
            "formulate a standalone question which can be understood "
            "without the chat history. Do NOT answer the question, just "
            "reformulate it if needed and otherwise return it as is."
        )
        chat_history_formatted = "\n".join(
            f"{entry['role']}: {entry['content']}" for entry in self.chat_history
        )
        prompt = (
            f"{context_prompt}\n\nChat history:\n{chat_history_formatted}\n\n"
            f"Present question: {question}"
        )
        return self._generate_response(prompt)

    def _generate_answer(self, question):
        """
        Generate an answer based on the resume content and the question.
        """
        qa_prompt = (
                f"""
                    You are simulating an interview based on the candidate's resume. Here is the candidate's resume: \n\n{self.resume_content}\n\n
                    Please adhere to the following rules while answering the interviewer's questions:
                    1) Provide answers strictly based on the resume content.
                    2) If a question cannot be answered with the resume, acknowledge it politely without introducing uncertainty (e.g., say, "I am not sure" or "This information is not available in my resume").
                    3) Ensure answers are polite, concise, and professional.
                    4) For simple questions, limit your response to 3 sentences.
                    5) For questions like 'Introduce yourself' or 'Explain your experiences,' respond within 120 words while highlighting key points from the resume.
                    6) Optimize answers to showcase relevant skills, achievements, and experiences.
                    7) If aptitude or technical questions are asked (e.g., on DSA), provide clear and structured explanations.
                    8) Avoid preamble, meta commentary, or any statements unrelated to the context of the resume.
                    9) Always ensure the tone is confident, articulate, and tailored to make a strong impression.
                    
                    Question: {question}
                """
            )

        return self._generate_response(qa_prompt)

    def generate_response(self, question):
        """
        Main method to generate a response by maintaining context.
        """
        # Reformulate the question with chat history
        standalone_question = self._contextualize_question(question)
        print("standalone_question", standalone_question)
        # Generate an answer based on the reformulated question
        answer = self._generate_answer(standalone_question)

        # Update chat history with the new interaction
        self.chat_history.append({"role": "user", "content": question})
        self.chat_history.append({"role": "bot", "content": answer})

        return answer

    def reset_chat_history(self):
        """
        Reset the chat history if starting a new conversation.
        """
        self.chat_history = []
