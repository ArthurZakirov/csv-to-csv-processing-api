from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from typing import Optional
import io
import httpx
from app.services.transform_service import process_csv

router = APIRouter()

@router.post(
    "/transform", 
    response_description="Transformed CSV file", 
    response_class=StreamingResponse
)
async def transform_csv(
    file_url: Optional[str] = Form(None),  # Accept file_url as a form field
    file: Optional[UploadFile] = File(None)
):
    # Check that at least one of `file` or `file_url` is provided
    if file is None and file_url is None:
        raise HTTPException(status_code=400, detail="Either file or file_url must be provided.")
    
    # If a URL is provided, download the CSV file
    if file_url:
        async with httpx.AsyncClient() as client:
            response = await client.get(file_url)
            if response.status_code != 200:
                raise HTTPException(status_code=400, detail="Could not fetch the file from the provided URL.")
            
            # Flexible check for 'text/csv' in Content-Type header
            content_type = response.headers.get("Content-Type", "")
            if "text/csv" not in content_type:
                raise HTTPException(status_code=400, detail="The URL does not point to a CSV file.")
            input_data = response.content
    
    # If an uploaded file is provided, read its content
    elif file:
        if "text/csv" not in file.content_type:
            raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV file.")
        input_data = await file.read()
    
    # Process the CSV data
    output_data = process_csv(input_data)

    # Return the processed CSV as a downloadable file
    response = StreamingResponse(
        io.StringIO(output_data),
        media_type="text/csv"
    )
    response.headers["Content-Disposition"] = "attachment; filename=transformed.csv"
    return response