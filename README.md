# AI Agent Chatbot with Function Calling

## 🚀 Project Overview
This project is an **AI Agent Chatbot with function calling capabilities**, designed to explore the feasibility of building **cost-effective, scalable AI agents** that can be deployed across a wide range of industries.

By leveraging **open-source language models** hosted via **Ollama**, we replicate the developer experience of using the **OpenAI SDK**, while significantly reducing costs and promoting flexibility.

The chatbot is structured to support rapid adaptation for different domains, making it highly reusable and extendable.

---

## 🛠️ Tech Stack

- **AI Model:** Open-Source LLMs via [Ollama](https://ollama.ai/)
- **Frontend:** Next.js (TypeScript)
- **Backend:** FastAPI (Python)
- **Programming Languages:** TypeScript, Python

---

## ✨ Key Features

- ✅ **Function Calling:** Enables the AI agent to trigger backend functions, similar to OpenAI's function calling system.
- ✅ **Open-Source Model Integration:** Easily swap out LLMs thanks to Ollama hosting.
- ✅ **WebSocket Communication:** Real-time chat experience using WebSockets.
- ✅ **File Upload Support:** Upload documents for AI-assisted processing.
- ✅ **Scalable Architecture:** Easily extendable to support additional tools, APIs, and domains.
- ✅ **Cost-Effective:** Optimized to reduce reliance on expensive proprietary APIs.

---

## 📂 Project Structure
Dynamic

## SetUP 


cd frontend
npm install
npm run dev


cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
pip install -r requirements.txt
uvicorn main:app --reload


🔗 WebSocket API
The chat system communicates with the backend via WebSocket for real-time interaction.

WebSocket URL: ws://<backend-host>/ws/{session_id}

📄 Future Improvements
 Multi-agent orchestration

 Industry-specific function packs

 Enhanced conversation memory

 Model fine-tuning support

 User authentication and session storage

 Vector database integration for retrieval-augmented generation (RAG)

🤝 Contributing
Contributions are welcome! Please open an issue or submit a pull request if you'd like to collaborate.

📜 License
This project is open-source and available under the MIT License.

🙌 Acknowledgments
Ollama for providing local LLM hosting.

The open-source AI community for driving accessible and affordable AI solutions.