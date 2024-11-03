from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from app.services.transform_service import process_csv
import io

router = APIRouter()

from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
import io

router = APIRouter()

@router.post(
    "/transform", 
    response_description="Transformed CSV file (update)", 
    response_class=StreamingResponse
)
async def transform_csv(file: UploadFile = File(...)):
    print(f"Detected content type: {file.content_type}")
    if file.content_type != "text/csv":
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV file.")
    
    # Read file and process
    input_data = await file.read()
    output_data = process_csv(input_data)  # Ensure this returns a CSV-formatted string

    # Prepare the response as a CSV file
    response = StreamingResponse(
        io.StringIO(output_data),
        media_type="text/csv"
    )
    response.headers["Content-Disposition"] = "attachment; filename=transformed.csv"
    return response