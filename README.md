# 📝 Streamlit To‑Do List Application

A simple, fast, and persistent To‑Do List web app built with [Streamlit](https://streamlit.io/).  
Tasks are saved to a local `todos.json` file so they **stay there even after you refresh, close the browser, or restart the app**.

---

## 🚀 Features

- **Add new tasks**
  - Title (required)
  - Priority: Low / Medium / High
  - Category: e.g. Work, Personal, School

- **Manage active tasks**
  - View all active to‑dos
  - Filter by **category** and **priority**
  - Mark tasks as **completed**
  - **Edit** existing tasks (title, category, priority)
  - Delete individual tasks

- **Manage completed tasks**
  - View all completed to‑dos
  - Filter by **category** and **priority**
  - Mark completed tasks as **incomplete** (move back to active)
  - Delete individual completed tasks
  - Clear **all** completed tasks at once

- **Analytics dashboard**
  - Total number of to‑dos
  - Completed vs remaining
  - Completion rate (%)
  - Priority distribution (bar chart)
  - Category distribution (pie chart)
  - Completion status (pie chart)

- **Persistent storage**
  - All tasks are stored in `todos.json` (same folder as the app file)
  - File is created automatically if it doesn’t exist

- **Extras**
  - Export current to‑dos as a JSON backup from the sidebar
  - Simple, clean UI with nice styling

---

## 🛠 Tech Stack

- **Python**
- **Streamlit** – web UI
- **Pandas** – simple data handling
- **Plotly Express** – charts for analytics
- **JSON** – persistent storage (`todos.json`)

---

## 📁 Project Structure

Example layout (your repo may have additional files):

```text
todostuff/
├── todo.py            # Main Streamlit app (entry point)
├── requirements.txt   # Python dependencies
└── todos.json         # Data file for tasks (auto-created)
