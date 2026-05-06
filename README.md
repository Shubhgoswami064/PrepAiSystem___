# PrepAI - AI-Powered Competitive Exam Preparation Platform

PrepAI is an intelligent, dynamic web application designed to help students prepare for competitive exams like UPSC, JEE, NEET, and SSC CGL. The platform leverages cutting-edge Generative AI (Google Gemini) to generate personalized quizzes and acts as an expert AI tutor for resolving student queries in real-time. It features a modern, premium UI with a glassmorphism aesthetic and provides insightful performance analytics.

---

## 🌟 Key Features

1. **AI Quiz Generation**: Dynamically creates customizable multiple-choice questions (MCQs) based on the selected exam type, subject, and difficulty level.
2. **AI Tutor Chatbot**: An intelligent conversational agent that provides expert guidance, explanations, and support to students.
3. **Performance Analytics**: Tracks user quiz results, calculates scores, and visualizes subject-wise progress and performance using dynamic charts.
4. **User Authentication**: Secure signup and login functionality.
5. **Interactive Dashboard**: A central hub for users to start quizzes, view past performance, and access the AI tutor.

---

## 🛠️ Technologies Used

### **Backend**
* **Python**: Core programming language.
* **Flask**: Lightweight web framework for handling routing, sessions, and API endpoints.
* **SQLite3**: Relational database for storing user credentials and quiz performance metrics.
* **Google Generative AI SDK**: Integrates the Gemini 2.5 Flash model for lightning-fast quiz generation and chat responses.

### **Frontend**
* **HTML5, CSS3, JavaScript**: Building blocks of the user interface.
* **Jinja2**: Templating engine used by Flask for dynamic HTML rendering.
* **Chart.js**: (Integrated in frontend) Used for rendering beautiful and dynamic performance analytic charts on the dashboard.

---

## 🔄 System Architecture & Data Flow

### 1. **Authentication Flow**
* Users sign up or log in via the `signup.html` / `login.html` interfaces.
* The frontend sends a `POST` request to `app.py`.
* Flask processes the data, validates it against the `bot_users` table in the SQLite database (`chatbot.db`), and creates a secure user session.

### 2. **AI Quiz Data Flow**
* **Request**: From the dashboard, users select parameters (Exam, Subject, Difficulty). The frontend sends a JSON `POST` request to the `/generate` endpoint in `app.py`.
* **Processing**: `app.py` passes the parameters to `ai_generator.py`. 
* **AI Generation**: `ai_generator.py` constructs a context-aware prompt (tailored to specific exam patterns like UPSC multi-statement or JEE technical depth) and calls the **Google Gemini API**.
* **Response**: The Gemini API returns a structured JSON array of questions, options, answers, and explanations. `ai_generator.py` parses this and passes it back to the frontend via Flask.
* **Submission**: Upon quiz completion, results are sent via `/submit-quiz` and stored in the `quiz_results` table in the database.

### 3. **AI Chatbot Data Flow**
* **Request**: User types a message in the `chatbot.html` interface.
* **Processing**: A JSON `POST` request containing the message and chat history is sent to `/chat`.
* **AI Interaction**: `ai_generator.py` manages the conversation history and queries the Gemini model using a custom "Expert AI Tutor" system instruction.
* **Response**: The AI's educational response is sent back to the frontend and appended to the chat window.

### 4. **Analytics Data Flow**
* The `/analytics-data` endpoint in `app.py` aggregates data from the `quiz_results` table for the logged-in user.
* It calculates the total score and percentage per subject and returns JSON data.
* The frontend JavaScript parses this data and renders visual graphs using Chart.js.

---

## 📂 Directory Structure & File Descriptions

```text
PrepAi/
│
├── app.py                  # Main Flask application, routes, API endpoints, and database logic.
├── ai_generator.py         # Core AI logic: Handles Google Gemini API calls, prompts, and JSON formatting.
├── chatbot.db              # SQLite Database containing 'bot_users' and 'quiz_results' tables.
├── config.py               # Auxiliary configuration file (legacy/secondary API keys).
├── test_gemini.py          # Testing script to verify Gemini API connection and response formats.
├── requirements.txt        # Python dependencies list.
├── .env                    # Environment variables (contains GEMINI_API_KEY).
│
└── templates/              # HTML templates rendered by Flask
    ├── base.html           # Base template with common layout, navbar, and styles.
    ├── welcome.html        # Landing page for unauthenticated users.
    ├── signup.html         # User registration page.
    ├── login.html          # User login page.
    ├── dashboard.html      # Main user hub showing analytics and navigation options.
    ├── quiz.html           # Interface for selecting quiz parameters and taking the test.
    └── chatbot.html        # AI Tutor chat interface.
```

---

## 🚀 Setup & Installation

### 1. Clone or Download the Repository
Navigate to the project directory in your terminal.

### 2. Create a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
Install all required Python packages using `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the root directory (if not already present) and add your Google Gemini API key:
```env
GEMINI_API_KEY="your_actual_api_key_here"
```

### 5. Run the Application
Start the Flask development server:
```bash
python app.py
```
The application will be accessible in your web browser at `http://127.0.0.1:5000`.

---

## 🎯 Usage Workflow for Faculty/Reviewers

1. **Launch**: Open `http://127.0.0.1:5000` to view the Welcome page.
2. **Onboarding**: Create an account via Signup, then Login.
3. **Dashboard**: Observe the layout. Analytics will be empty initially.
4. **Take a Quiz**: Navigate to the Quiz section, select parameters (e.g., UPSC, History, Medium), and let the AI generate the test. Submit the test.
5. **Check Analytics**: Return to the Dashboard to see how the database updates and the Chart.js graphs visualize the recent test scores.
6. **Test the Tutor**: Navigate to the Chatbot and ask an exam-related conceptual question to test the customized Gemini prompt.
