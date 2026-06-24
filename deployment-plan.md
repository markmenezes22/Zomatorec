# Deployment Plan: Zomato Recommendation Engine

This document outlines the steps required to deploy the project using **Railway** for the FastAPI backend and **Vercel** for the static frontend.

## 1. Prerequisites
- The code must be pushed to your GitHub repository (`https://github.com/markmenezes22/Zomatorec`).
- Accounts on [Railway.app](https://railway.app/) and [Vercel.com](https://vercel.com/).

---

## 2. Backend Deployment (Railway)

Railway is excellent for Python web services and will automatically detect your `requirements.txt`.

### Steps:
1. **Create a New Project:** Log into Railway, click **New Project** -> **Deploy from GitHub repo**, and select the `Zomatorec` repository.
2. **Configure Service:**
   - Go to the **Settings** tab of your new service.
   - **Root Directory**: Leave it as `/` (root).
   - **Start Command**: Set the custom start command to bind to Railway's dynamic port:
     ```bash
     uvicorn src.main:app --host 0.0.0.0 --port $PORT
     ```
3. **Environment Variables:**
   - Go to the **Variables** tab.
   - Add all the variables from your local `.env` file:
     - `GROQ_API_KEY` (Your actual Groq API key)
     - `GROQ_MODEL` (e.g., `llama-3.3-70b-versatile`)
     - `GROQ_TEMPERATURE` (e.g., `0.3`)
     - `MAX_CANDIDATES_FOR_LLM` (e.g., `15`)
     - `TOP_K_RECOMMENDATIONS` (e.g., `5`)
     - `HF_DATASET_NAME` (e.g., `ManikaSaini/zomato-restaurant-recommendation`)
     - `DATA_CACHE_PATH` (e.g., `data/zomato_cache.parquet`)
     - `BUDGET_LOW_MAX` (e.g., `500`)
     - `BUDGET_MEDIUM_MAX` (e.g., `1500`)
4. **Generate Public Domain:**
   - In the **Settings** tab, scroll down to **Domains** and click **Generate Domain** (or add your custom domain).
   - **Important:** Save this URL (e.g., `https://zomatorec-production.up.railway.app`). You will need it for the frontend.

---

## 3. Frontend Deployment (Vercel)

Vercel is perfect for serving the static files (`index.html`, `app.js`, etc.) located in your `frontend/` directory.

### Preparation Step (Local)
Before deploying the frontend, you must update the API base URL in your frontend code so it points to your new Railway backend.
1. Open `frontend/app.js`.
2. Change the `API_BASE` constant on line 1 from `http://localhost:8000/api` to your Railway domain:
   ```javascript
   const API_BASE = 'https://<your-railway-domain>.up.railway.app/api';
   ```
3. Commit and push this change to GitHub:
   ```bash
   git add frontend/app.js
   git commit -m "Update API_BASE for production"
   git push origin main
   ```

### Steps:
1. **Create a New Project:** Log into Vercel, click **Add New...** -> **Project**, and import your `Zomatorec` GitHub repository.
2. **Configure Project:**
   - **Project Name:** `zomatorec-frontend` (or any name you prefer).
   - **Framework Preset:** Leave as `Other` (since it's vanilla HTML/JS).
   - **Root Directory:** Click Edit and select `frontend`. Vercel will serve files directly from this folder.
   - **Build Command:** Leave blank.
   - **Output Directory:** Leave blank.
3. **Deploy:** Click the **Deploy** button. Vercel will instantly publish your site and provide you with a production URL (e.g., `https://zomatorec-frontend.vercel.app`).

---

## 4. Post-Deployment Verification

1. **Test the API:** Open your Railway backend URL + `/api/metadata/locations` in the browser to ensure the backend is running and returning data.
2. **Test the UI:** Open your Vercel frontend URL, ensure the form loads correctly, and test generating a recommendation.
3. **CORS Check:** If your frontend fails to fetch data, verify that `src/main.py` has `allow_origins=["*"]` or specifically includes your Vercel URL in the CORS middleware configuration. (Currently, it is set to `["*"]`, which will work perfectly out-of-the-box).
