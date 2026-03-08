# ☁️ Deploying Full-Stack AI Learning Lab to Render (Free Tier)

This repository includes a `Dockerfile` that serves both the **HTML Dashboard** and the **FastAPI Python Backend**. 

You can deploy this to Render in just a few minutes, completely for **free**:

### 🎯 Step-by-Step Deployment Guide
1. Create a free account on [Render.com](https://render.com).
2. Click the **New +** button in the top right corner and select **Web Service**.
3. Choose **Build and deploy from a Git repository**.
4. Connect your GitHub account and select this repository (`ai-learning-langchain-agents`).
5. In the configuration settings, specify:
   * **Name:** `ai-learning-dashboard` (or any unique name you prefer)
   * **Branch:** `main`
   * **Environment:** `Docker` (This is very important!)
   * **Instance Type:** `Free`

### 🔑 CRITICAL STEP: Add Your API Key
Because your website now connects directly to real LangChain backend code, the server **must** have an OpenAI key to function. 
* Scroll down to **Environment Variables**.
* Click **Add Environment Variable**.
* **Key:** `OPENAI_API_KEY`
* **Value:** `sk-proj... (Your actual OpenAI API Key)`

6. Click **Create Web Service**.

---

### 🏗️ How the Architecture Works Under the Hood
1. **The Docker Image:** The `Dockerfile` pulls an official Python image, installs all your required dependencies (`requirements.txt` including LangChain and FastAPI), and copies all your code into the container.
2. **The Server:** When Render boots the container, it runs `uvicorn server:app`. This is a professional-grade asynchronous web server.
3. **The Frontend:** If the user visits the standard URL (`/`), FastAPI will use `StaticFiles` to serve the visual `index.html` dashboard natively.
4. **The Backend AI:** When a user clicks "Execute Research" or uses the Playground, Javascript shoots an HTTP POST request to `/api/research` or `/api/playground`. The FastAPI server intercepts this, dynamically imports your actual module scripts (`01_hello_langchain.py`, etc.), queries GPT-4o-mini using your loaded API key, and perfectly formats the JSON response back to the shiny UI widget on the screen!

*This ensures the code your learners read on the screen is the **exact same code executing live.** *
