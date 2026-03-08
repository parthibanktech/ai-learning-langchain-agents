# ☁️ Deploying to Render Cloud (Free Tier)

This repository includes a `Dockerfile` specifically designed to serve the Interactive Learning Dashboard quickly and securely using **Nginx**.

You can deploy this to Render in less than 5 minutes for **free**:

### Step-by-Step Guide
1. Create a free account on [Render.com](https://render.com).
2. Click the **New +** button in the top right corner and select **Web Service**.
3. Choose **Build and deploy from a Git repository**.
4. Connect your GitHub account and select this repository: `ai-learning-langchain-agents`.
5. In the configuration settings, specify:
   * **Name:** `ai-learning-dashboard` (or any unique name you prefer)
   * **Branch:** `main`
   * **Environment:** `Docker` (This is very important!)
   * **Instance Type:** `Free`
6. Click **Create Web Service**.

### How it Works Under the Hood
The `Dockerfile` in this repo grabs a lightweight `nginx:alpine` image and copies only the frontend files (`index.html`, `app.js`, `*.css`). It completely ignores the Python backend server (`venv`, `.env`, `*.py`) using the rules defined in `.dockerignore`. 

This ensures your API Keys and large local environments are never uploaded to the public cloud, while still giving your users a beautiful, responsive web dashboard!
