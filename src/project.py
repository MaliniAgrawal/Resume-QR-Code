import qrcode

# Define the path to your resume document file in the Windows file system
resume_file_path = 'src/maliniresume-2023.docx'

# Generate a QR code for the resume document file
qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
qr.add_data(resume_file_path)
qr.make(fit=True)

# Create an image from the QR code
qr_image = qr.make_image(fill_color="black", back_color="white")

# Save the QR code image
qr_image.save('resume_qr_code.png')

print("QR code generated successfully!")
