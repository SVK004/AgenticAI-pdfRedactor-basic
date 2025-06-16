from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from redactor import redact_file
import shutil
import uuid
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
os.makedirs("temp", exist_ok=True)

@app.post("/")
async def upload_pdf(file: UploadFile = File(...)):
    input_path = f"temp/{uuid.uuid4()}.pdf"
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    output_path = input_path.replace(".pdf", "_redacted.pdf")
    print("INPUT FILE RECEIVED AND SENDING TO REDACT BROSKIII")
    redact_file(input_path, output_path)

    return FileResponse(output_path, media_type = "application/pdf", filename = "redacted.pdf")