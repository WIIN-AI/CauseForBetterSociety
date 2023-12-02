# CauseForBetterSociety
CauseForBetterSociety - this is repo to server the one of the NGO. Which is working cause for better society.

### Create a new directory for your project and initialize a virtual environment:
mkdir news_feed_app
cd news_feed_app
python -m venv venv

- On Windows
  - venv\Scripts\activate
- On Unix or MacOS:
  - source venv/bin/activate

# Run the requirements.txt
- pip install -r requirements.txt OR pip install fastapi uvicorn

# to start the app in local host : 8000
- `uvicorn main:app --reload`

# to access all the END POINTS 
- http://127.0.0.1:8000/docs