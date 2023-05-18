import jinja2
import pdfkit
from fastapi import Depends,APIRouter,HTTPException,status
from app import models
from ..database import get_db
from app import oauth2
from sqlalchemy.orm import Session
import os
from io import BytesIO
from fastapi.responses import StreamingResponse,JSONResponse

router = APIRouter(tags=['Pdf'])

#print 
@router.post("/print")
def print(current_user: models.User = Depends(oauth2.get_current_user), db:Session = Depends(get_db)):

    data = db.query(models.UserDetail).filter(models.UserDetail.user_id == current_user.id).first()
    if data is None:
        raise HTTPException(detail= 'invalid credentials or user profile was not created', status_code=status.HTTP_403_FORBIDDEN)
    
    first_name = current_user.first_name
    last_name = current_user.last_name
    bio = data.bio
    gender = data.gender
    address = data.address
    phone_number = current_user.phone_number

    context = {'first_name': first_name, 'last_name': last_name, 'bio': bio, 'gender': gender, 'address': address, 'phone_number': phone_number}

    template_loader = jinja2.FileSystemLoader(r'C:\Users\CS0142302.CSVIZAG\Documents\MyfastAPI2\app\routers')
    template_env = jinja2.Environment(loader=template_loader)

    template = template_env.get_template('basic-template.html')
    output_text = template.render(context)

    config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
    pdf_context =  pdfkit.from_string(output_text, False, configuration=config)

      # Create BytesIO stream
    pdf_stream = BytesIO(pdf_context)

    # Move the stream position to the beginning
    pdf_stream.seek(0)
    
    filename = "example.pdf"
    with open(filename, "wb") as f:
        f.write(pdf_stream.getbuffer())

    # Get the absolute path of the PDF file
    file_path = os.path.abspath(filename)

    return JSONResponse({"filename": filename, "file_path": file_path})






















    # Return the PDF file as a response
    # return StreamingResponse(pdf_stream, media_type='application/pdf', headers={'Content-Disposition': 'attachment; filename="pdf_generated.pdf"'})


    # # Generate a temporary file path
    # file_path = tempfile.mktemp(suffix='.pdf')

    # # Write the PDF content to the file
    # with open(file_path, 'wb') as file:
    #  file.write(pdf_context)

    # # Return the file name and path in the response
    # return {'file_path': file_path, 'file_name': 'pdf_generated.pdf'}
