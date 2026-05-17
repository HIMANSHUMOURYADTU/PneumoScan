# Deploying PneumoScan on Vercel

This application is ready to be deployed to Vercel's Python Serverless environment.

## ⚠️ Important Note About Vercel's Limits
Vercel's Serverless Functions have a **250 MB** uncompressed size limit. Because this project uses `tensorflow` (via `tensorflow-cpu`), `numpy`, and an `.h5` model file, the total size of your application might exceed this limit.

If Vercel throws a "function size too large" error during build:
You will need to host this on a platform designed for Machine Learning models, such as:
* [Render](https://render.com)
* [Railway](https://railway.app)
* [Hugging Face Spaces](https://huggingface.co/spaces)

## Step-by-Step Vercel Deployment

1. **GitHub Repository**:
   Make sure all your files (`app.py`, `vercel.json`, `requirements.txt`, `pneumonia_classifier.h5`, and `templates/index.html`) are pushed to a repository on GitHub.

2. **Connect to Vercel**:
   - Go to [vercel.com](https://vercel.com/) and create a new project.
   - Click "Import third-party Git Repository" or link your GitHub account.
   - Select your `PneumoScan` repository.

3. **Deploy**:
   - Vercel automatically detects the `vercel.json` file.
   - You don't need to change any build commands.
   - Click **Deploy**. Vercel will install dependencies from `requirements.txt` and map your Python app.
