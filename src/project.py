import os
import boto3
import docx
import qrcode
from io import BytesIO

def generate_qr_code(event, context):
    # Extract the file from the Lambda event
    file_object = event['file']

    # Convert the binary file data to a Docx file
    docx_file = BytesIO(file_object)
    document = docx.Document(docx_file)

    # Extract text from the document
    resume_text = ""
    for paragraph in document.paragraphs:
        resume_text += paragraph.text + "\n"

    # Generate the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(resume_text)
    qr.make(fit=True)

    qr_code_image = qr.make_image(fill_color="black", back_color="white")

    # Save the QR code to a BytesIO object
    qr_code_bytes_io = BytesIO()
    qr_code_image.save(qr_code_bytes_io, format="PNG")
    qr_code_bytes_io.seek(0)

    # Upload the QR code image to an S3 bucket
    s3_bucket_name = "your-s3-bucket-name"
    qr_code_filename = "resume_qr_code.png"

    s3_client = boto3.client('s3')
    s3_client.put_object(
        Bucket=s3_bucket_name,
        Key=qr_code_filename,
        Body=qr_code_bytes_io.read(),
        ContentType="image/png"
    )

    # Return the S3 URL of the generated QR code
    qr_code_url = f"https://{s3_bucket_name}.s3.amazonaws.com/{qr_code_filename}"
    return {
        "statusCode": 200,
        "body": qr_code_url
    }
