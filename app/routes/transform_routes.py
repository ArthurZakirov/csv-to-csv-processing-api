from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from app.services.transform_service import process_csv
import io

router = APIRouter()

@router.post("/transform", response_description="Transformed CSV file")
async def transform_csv(file: UploadFile = File(...)):
    if file.content_type != "text/csv":
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV file.")
    
    # Read file and process
    input_data = await file.read()
    output_data = process_csv(input_data)

    # Prepare the response as a CSV file
    response = StreamingResponse(
        io.StringIO(output_data),
        media_type="text/csv"
    )
    response.headers["Content-Disposition"] = "attachment; filename=transformed.csv"
    return response