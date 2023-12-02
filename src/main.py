# from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
# from fastapi.responses import JSONResponse
# from fastapi.middleware.cors import CORSMiddleware
# from motor.motor_asyncio import AsyncIOMotorClient
# from dotenv import load_dotenv
# from starlette.requests import Request
# import boto3
# import os
#
# load_dotenv()
#
# app = FastAPI()
#
# # Enable CORS for all origins
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
#
# # MongoDB
# mongo_uri = os.getenv("MONGO_URI")
# client = AsyncIOMotorClient(mongo_uri)
# db = client.get_database()
#
# # S3
# s3_bucket_name = os.getenv("S3_BUCKET_NAME")
# aws_region = os.getenv("AWS_REGION")
# s3_client = boto3.client("s3", region_name=aws_region)
#
#
# @app.post("/upload")
# async def upload_file(file: UploadFile = File(...), description: str = ""):
#     # Save file to S3
#     s3_key = f"images/{file.filename}"
#     s3_client.upload_fileobj(file.file, s3_bucket_name, s3_key)
#
#     # Save metadata to MongoDB
#     collection = db.news_feed
#     result = await collection.insert_one({"image_url": f"https://{s3_bucket_name}.s3.amazonaws.com/{s3_key}", "description": description})
#
#     return JSONResponse(content={"message": "File uploaded successfully", "id": str(result.inserted_id)})
#
#
# @app.get("/news_feed")
# async def get_news_feed():
#     # Retrieve news feed from MongoDB
#     collection = db.news_feed
#     news_feed = await collection.find().to_list(length=10)
#
#     return news_feed
#
#
# @app.post("/comment/{news_id}")
# async def add_comment(news_id: str, comment: str):
#     # Add comment to the specified news entry in MongoDB
#     collection = db.news_feed
#     result = await collection.update_one({"_id": news_id}, {"$push": {"comments": comment}})
#
#     if result.modified_count == 0:
#         raise HTTPException(status_code=404, detail="News entry not found")
#
#     return {"message": "Comment added successfully"}
