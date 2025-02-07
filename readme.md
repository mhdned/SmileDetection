# Smile Detection

> FastAPI-based Image Processing Application

## Overview

**Smile Detection** is a FastAPI-based web application that allows users to upload images for processing using AI models. The application supports file uploads, processes images, and returns results to the client.

## Features

- Upload PNG and JPG images for processing
- AI-based image analysis using a pre-trained model
- Serve processed files for download
- Simple HTML-based frontend using Jinja2 templates
- Static file handling via FastAPI

## Installation

### Prerequisites

- Python 3.8+
- FastAPI
- Uvicorn (for running the server)
- OpenCV (cv2) for image processing
- NumPy for numerical computations
- Joblib for loading the AI model

### Setup Instructions

1. Clone the repository:
   ```sh
   git clone https://github.com/mhdned/SmileDetection.git
   cd SmileDetection
   ```
2. Create a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run the application:
   ```sh
   uvicorn main:app --reload
   ```

## API Endpoints

### Check API Status

**Endpoint:** `GET /`

- Returns an HTML page confirming that the API is live.

### Upload and Process Image

**Endpoint:** `POST /process`

- Accepts an image file (PNG, JPG) and processes it using the AI model.
- Returns an HTML response with the processed result.

### Download Processed File

**Endpoint:** `GET /file/{file_name}`

- Allows users to download processed files.

## AI Model

The application utilizes an AI model stored in `smile.z`, which is loaded using Joblib. The model is used to analyze images and classify them accordingly. The AI logic is implemented in `core/ai.py`:

```python
import cv2
from joblib import load
import numpy as np

clf = load("smile.z")

def load_pic(item):
    img = cv2.imread(item)
    img_r = cv2.resize(img,(32,32))
    img_r = img_r / 255
    img_r = img_r.flatten()
    img_r = np.array([img_r])

    label = clf.predict(img_r)[0]
    return label
```

## Project Structure

```
├── main.py            # Main application file
├── core/
│   ├── ai.py          # AI model integration
│   ├── jinja.py       # Jinja template engine configuration
├── static/            # Static files (CSS, JS, images)
├── templates/         # HTML templates
├── uploads/           # Uploaded images
├── requirements.txt   # Python dependencies
├── README.md          # Project documentation
```

## Technologies Used

<p align="left">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=python,fastapi" />
  </a>
</p>

## License

This project is licensed under the MIT License. See `LICENSE` for details.

## Author

Developed by [Mehtiuo](https://github.com/mhdned) & Root313.
