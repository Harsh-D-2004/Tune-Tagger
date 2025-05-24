# 🎵 Tune Tagger

**Tune Tagger** is a powerful tool designed to identify and timestamp specific songs or music pieces within videos. It's especially useful for content creators, music enthusiasts, and educators who want to explore, analyze, or credit audio content in video formats.

---

## Features

- **🎧 Song Detection**: Combines a custom deep learning model with the Shazam API for accurate song identification.
- **⏱️ Timestamps**: Mark and retrieve exact video timestamps where music is detected.
- **🧩 Chrome Extension**: Seamless browser integration with an easy-to-use UI.
- **🔊 Audio Extraction**: Extracts and analyzes audio from video files for identification.

---

## Technologies Used

### Backend
- **Framework**: Django
- **Database**: PostgreSQL
- **Deep Learning Model**: Custom deep learning models for audio analysis and prediction

### Frontend
- Built using JavaScript and Chrome APIs
- React

---

## Backend Setup

### 1. Install Dependencies

```bash
# Navigate to backend
cd Tune-Tagger-backend

# Install Python dependencies
pip install -r requirements.txt

python manage.py runserver
```

## Database Configuration

### Ensure PostgreSQL is running and configured as follows:

```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'musicautomation',
        'USER': 'postgres',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Frontend Setup

### Install Dependencies

```bash
# Navigate to frontend
cd Tune-tagger-frontend

# Install Node dependencies
npm install
```
## Screenshots

### Start Development Server

```bash
npm run dev
```
