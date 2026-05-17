# PneumoScan

PneumoScan is an AI-powered diagnostic web application built with Flask and TensorFlow that detects pneumonia from chest X-rays.

## Deploying on Vercel

This repository is already pre-configured for Vercel Serverless deployment via the included `vercel.json`.

### ⚠️ Important Note About Vercel's Size Limits
Vercel's Serverless Functions (AWS Lambda) have a strict **250 MB** uncompressed size limit. Because this project uses `tensorflow` (even the restricted `tensorflow-cpu` version) and numeric libraries like `numpy` alongside an `.h5` weights file, you *might* exceed this limit during deployment. If Vercel throws a "function size too large" error during build, you will need to host this on a platform designed for ML workloads, such as [Render](https://render.com), [Railway](https://railway.app), or [Hugging Face Spaces](https://huggingface.co/spaces).

### Deployment Steps

1. **Push to GitHub**:
   Ensure all your code (including `app.py`, `vercel.json`, `requirements.txt`, and your model `pneumonia_classifier.h5`) is pushed to a Github repository.
   
2. **Import to Vercel**:
   - Go to [vercel.com](https://vercel.com/) and create a new project.
   - Select "Import third-party Git Repository" and authorize GitHub if you haven't already.
   - Choose the `PneumoScan` repository.

3. **Deploy**:
   - Leave all build settings as default (Vercel automatically detects the `vercel.json` config).
   - Click **Deploy**.
   - Vercel will install the dependencies from `requirements.txt` and launch the app.

---

## Local Development

If you want to run this application locally:

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Place your `pneumonia_classifier.h5` in the root directory.
3. Run the Flask server:
   ```bash
   python app.py
   ```
4. Open your browser and navigate to `http://localhost:5000`.