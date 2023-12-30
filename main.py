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
import uuid
import datetime


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
comments_storage_path = os.path.join(ROOT_DIR, "comments")
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

async def add_image(file: UploadFile = File(...),
                    heading: str = None, description: str = None,
                    user_visibility: bool = True, location: str = None, email: str = None):
    with open(f"{image_storage_path}/{file.filename}", "wb") as image:
        image.write(file.file.read())
    uuid_ = str(uuid.uuid4())
    # Fetch the current date and time
    now = datetime.datetime.now()
    today_date = now.strftime("%d-%m-%Y")
    # Add image information to the comments file
    image_info = {"filename": file.filename,
                  "uuid": uuid_,
                  "heading": heading,
                  "description": description,
                  "comments": [],
                  "user_visibility": user_visibility,
                  "location": location,
                  'date' : today_date,
                  "like": None,
                  "email": email
                  }
    print(image_info)
    with open(comments_file, "r") as f:
        comments = json.load(f)

    comments[uuid_] = image_info

    with open(comments_file, "w") as f:
        json.dump(comments, f)

    return JSONResponse(content={"message": "Image added successfully"})


@app.post("/add_comment")
async def add_comment(image_id: str, comment: str):
    # Add a comment to the image in the comments file
    with open(comments_file, "r") as f:
        _data = json.load(f)

    if image_id in _data:
        _data[image_id]["comments"].append(comment)

        with open(comments_file, "w") as f:
            json.dump(_data, f)

        return JSONResponse(content={"message": "Comment added successfully"})
    else:
        return JSONResponse(content={"message": "Image not found"}, status_code=404)


@app.get("/get_images")
async def get_images():
    # Retrieve all images and their information
    with open(comments_file, "r") as f:
        comments = json.load(f)

    image_list = [{
        "image_id": info["uuid"],
        "filename": info["filename"],
        "description": info["description"],
        "heading": info["heading"],
        "user_visibility" : info["user_visibility"],
        "date" : info["date"],   
        "email" : info["email"]     
    } for info in comments.values()]

    return JSONResponse(content=image_list)


@app.get("/get_comments")
async def get_comments(image_id: str):
    # Retrieve comments for a specific image
    with open(comments_file, "r") as f:
        _data = json.load(f)

    if image_id in _data:
        return JSONResponse(content={"comments": _data[image_id]["comments"]})
    else:
        return JSONResponse(content={"message": "Image not found"}, status_code=404)


@app.get("/get_single_incident_details")
async def single_incident_details(image_id: str):
    # Retrieve comments for a specific image
    with open(comments_file, "r") as f:
        _data = json.load(f)

    if image_id in _data:
        return JSONResponse(_data[image_id], status_code=200)
    else:
        return JSONResponse(content={"message": f"Image {image_id} not found"}, status_code=404)


@app.get("/get_all_incident_details")
async def single_incident_details():
    try:
        # Retrieve comments for a specific image
        with open(comments_file, "r") as f:
            _data = json.load(f)
        return JSONResponse(_data, status_code=200)
    except Exception as ex:
        return JSONResponse(content={"message": ex}, status_code=404)


@app.get("/like_status")
async def like_status_update(image_id: str, is_liked: bool):    
    with open(comments_file, "r") as f:
        comments = json.load(f)

    if is_liked:
        comments[image_id]["like"] = comments[image_id]["like"] - 1
    else:
        comments[image_id]["like"] = comments[image_id]["like"] + 1

    if image_id in comments:
        return JSONResponse(content={"comments": comments[image_id]}, status_code=200)
    else:
        return JSONResponse(content={"message": f"Image {image_id} not found"}, status_code=404)


@app.post("/genai/chat")
async def genai_chat(user_query: str):
    try:
        print("user input query ", user_query)
        return JSONResponse(content={"answer": "sample GEN AI response"}, status_code=200)
    except Exception as ex:
        print(ex)
        return JSONResponse(content={"message": "Image not found"}, status_code=404)


@app.post("/genai/upload_document")
async def genai_upload_document(file: UploadFile = File(...), session_id: str = Form(...)):
    try:
        with open(f"{image_storage_path}/{file.filename}", "wb") as image:
            image.write(file.file.read())
            print(session_id)
        return JSONResponse(content={"message": f"upload_document Done :{file.filename}"}, status_code=200)
    except Exception as ex:
        print(ex)
        return JSONResponse(content={"message": "upload_document Failed"}, status_code=404)


@app.delete("/genai/delete_all_document")
async def genai_delete_all_document(session_id: str):
    try:
        return JSONResponse(content={"message": f"delete_all_document {session_id} DONE"}, status_code=200)
    except Exception as ex:
        print(ex)
        return JSONResponse(content={"message": "delete_all_document Failed"}, status_code=404)


@app.get("/genai/get_all_documents")
async def gen_ai_get_all_documents(session_id:str):
    try:
        print(session_id)
        list_docs = ["SAMPLE_DOC_01", "SAMPLE_DOC_02"]
        return JSONResponse(content={"documents": list_docs}, status_code=200)
    except Exception as ex:
        print(ex)
        return JSONResponse(content={"message": []}, status_code=404)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
