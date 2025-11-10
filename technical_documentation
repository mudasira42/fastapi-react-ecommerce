# 🧱 System Architecture — FastAPI + React 19 E-Commerce App

Below is the technical architecture of the **FastAPI + React 19 E-Commerce Web Application**:

![System Architecture](./architecture-diagram.png)

---

## 🧠 Overview

This full-stack system connects a **React 19 frontend** with a **FastAPI backend** and a **MongoDB Atlas database**.  
- The frontend (React + Tailwind + shadcn/ui) handles UI, routing, and global state management with Context API.  
- The backend (FastAPI) exposes RESTful APIs, performs authentication (JWT + bcrypt), and manages asynchronous database operations using Motor.  
- MongoDB Atlas stores users, products, and cart data.

---

## ⚙️ Data Flow

1. User interacts with the React frontend.  
2. Axios sends API requests to FastAPI (hosted on Render).  
3. FastAPI validates data using Pydantic and interacts asynchronously with MongoDB Atlas.  
4. The API returns JSON responses to the frontend for rendering.  
5. JWT tokens secure authentication routes; cart state is synced between local storage and backend.

---

## 🧩 Key Components

| Layer | Tech Stack | Responsibilities |
|--------|-------------|------------------|
| **Frontend** | React 19, Tailwind CSS, shadcn/ui, React Router v7 | Product browsing, cart management, authentication UI |
| **Backend** | FastAPI, Python-JOSE, bcrypt, Pydantic | REST API, authentication, data validation |
| **Database** | MongoDB Atlas with Motor | Stores products, users, and cart information |

---

## 🚀 Deployment

| Component | Platform | Notes |
|------------|-----------|-------|
| **Frontend** | Vercel | `npm run build` → deploy build folder |
| **Backend** | Render / Railway | `uvicorn server:app --host 0.0.0.0 --port $PORT` |
| **Database** | MongoDB Atlas | Cloud-hosted cluster connected via secure URI |

---

**📄 File:** `docs/architecture.md`  
**📁 Diagram:** `docs/architecture-diagram.png`

---

✅ Once committed, your GitHub repo will show the image directly in the Markdown file!

---

### ⚡ Step 4: Commit & Push

Run these commands in your terminal (inside project root):

```bash
git add docs/architecture-diagram.png docs/architecture.md
git commit -m "Added technical architecture diagram and documentation"
git push
