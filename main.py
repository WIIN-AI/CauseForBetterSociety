from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import json
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from starlette.requests import Request
import boto3
import os
from typing import List

from rootdir import ROOT_DIR

app = FastAPI(debug=True)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://0.0.0.0:8080",
]

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store images in a file manager
image_storage_path = os.path.join(ROOT_DIR, "image_storage")
# Create image storage directory if it doesn't exist
if not os.path.exists(image_storage_path): os.makedirs(image_storage_path)

# Store comments in a file manager
comments_storage_path = os.path.join(ROOT_DIR, "Comments")
comments_file = os.path.join(comments_storage_path, "comments.json")
# Create Comments storage directory if it doesn't exist
if not os.path.exists(comments_storage_path): os.makedirs(comments_storage_path)

try:
    with open(comments_file, "r") as f:
        pass
except FileNotFoundError:
    # Create an empty comments file if it doesn't exist
    if not os.path.exists(comments_file):
        with open(comments_file, "w") as f:
            json.dump({}, f)


@app.post("/add_image/")
async def add_image(file: UploadFile = File(...), description: str = Form(...), ):
    # Save the image to the file manager
    with open(f"{image_storage_path}/{file.filename}", "wb") as image:
        image.write(file.file.read())

    # Add image information to the comments file
    image_info = {"filename": file.filename, "description": description, "comments": []}
    with open(comments_file, "r") as f:
        comments = json.load(f)

    comments[file.filename] = image_info

    with open(comments_file, "w") as f:
        json.dump(comments, f)

    return JSONResponse(content={"message": "Image added successfully"})


@app.post("/add_comment/{filename}")
async def add_comment(filename: str, comment: str):
    # Add a comment to the image in the comments file
    with open(comments_file, "r") as f:
        comments = json.load(f)

    if filename in comments:
        comments[filename]["comments"].append(comment)

        with open(comments_file, "w") as f:
            json.dump(comments, f)

        return JSONResponse(content={"message": "Comment added successfully"})
    else:
        return JSONResponse(content={"message": "Image not found"}, status_code=404)


@app.get("/get_images/")
async def get_images():
    # Retrieve all images and their information
    with open(comments_file, "r") as f:
        comments = json.load(f)

    image_list = [{"filename": info["filename"], "description": info["description"]} for info in comments.values()]

    return JSONResponse(content=image_list)


@app.get("/get_comments/{filename}")
async def get_comments(filename: str):
    # Retrieve comments for a specific image
    with open(comments_file, "r") as f:
        comments = json.load(f)

    if filename in comments:
        return JSONResponse(content={"comments": comments[filename]["comments"]})
    else:
        return JSONResponse(content={"message": "Image not found"}, status_code=404)


@app.post("/genai/chat")
async def genai_chat(user_query: str):
    try:
        print("user input query ", user_query)
        return JSONResponse(content={"message": "sample GEN AI response"},status_code=200)
    except Exception as ex:
        print(ex)
        return JSONResponse(content={"message": "Image not found"}, status_code=404)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
