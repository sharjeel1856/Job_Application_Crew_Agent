# 🤖 Job Application Crew

AI-powered web application that **automatically generates tailored resumes** and **interview preparation materials** based on job postings and candidate profiles — powered by **CrewAI Agents**, **FastAPI**, and **OpenAI GPT**.

---

## 📸 Screenshots

![7ec41c4e0b144ece84ef31d3c184f109](https://github.com/user-attachments/assets/85afe7a8-8a9a-4bd0-8825-e9cf60de34e9)

 ![2df2576601124963aa3b6959830877f8](https://github.com/user-attachments/assets/82f7f156-0d1d-4c8b-ba18-87c7b8991178)

![90abb37bd3e944e4b628adc690f16cd8](https://github.com/user-attachments/assets/41c78beb-e7cc-4d96-8d19-fe7c4190b6d2)

![b3a63069911e4401a0d65a1b6c2efacd](https://github.com/user-attachments/assets/936630fc-dc8e-41aa-a578-6543b0d398af)

![870c39d53c654262b1da9aaca60c17bf](https://github.com/user-attachments/assets/ee9f7e1f-0b52-4d78-82df-479e5012151a)

![6b0e9024e6644de08bd271ed0b085ec5](https://github.com/user-attachments/assets/ceeac8f9-a828-41c6-b3c2-7d2def9fde84)

![8863315e60ae44d5ab3a53385b731b37](https://github.com/user-attachments/assets/ac05fe30-e73c-4e6f-9497-951955327bc8)

![c989d569d8874a16a1c79013ee80d47d](https://github.com/user-attachments/assets/05726fea-bff8-4697-ace2-38d82e6e7c2d)

---

## 🛠️ Features

- 📝 **Resume Generation** – Tailored, job-specific resumes in markdown format.
- 🎯 **Interview Prep** – STAR-method responses & behavioral questions.
- 🔍 **Job Analysis** – Extracts skills, qualifications, and requirements from job postings.
- 👨‍💻 **Profile Building** – Integrates GitHub & LinkedIn profile analysis.
- 📂 **Secure File Download** – Download resumes & interview materials safely.
- 📱 **Responsive UI** – Works on desktop, tablet, and mobile.

---

## 🛠️ Tech Stack

- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Backend:** Python 3.10+, FastAPI
- **AI:** CrewAI, OpenAI GPT
- **Database:** ChromaDB
- **File Storage:** Local file system

---

## 📦 Installation

```bash
# 1️⃣ Clone this repository
git clone https://github.com/YourUsername/JobApplicationCrew.git
cd JobApplicationCrew

# 2️⃣ Create a virtual environment
python -m venv venv
source venv/bin/activate  # (Linux/Mac)
venv\Scripts\activate     # (Windows)

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Create .env file and add your API keys
OPENAI_API_KEY=your_openai_key
SERPER_API_KEY=your_serper_key

# 5️⃣ Run the server
uvicorn main:app --reload
![7ec41c4e0b144ece84ef31d3c184f109](https://github.com/user-attachments/assets/29437ccb-c931-4399-a111-99f6fcd19ac7)
