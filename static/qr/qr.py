import qrcode
import os

def generate_qr(user_email):
    # Create folder if it doesn't exist
    qr_folder = os.path.join(os.path.dirname(__file__))
    if not os.path.exists(qr_folder):
        os.makedirs(qr_folder)

    # Create a QR Code instance
    qr = qrcode.QRCode(
        version=1,  # Smallest size
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )

    # Add user-specific data (e.g., URL or user info)
    data = f"https://yourapp.com/user/{user_email}"  # Replace with actual link logic
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image from the QR Code
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image
    qr_filename = f"{user_email.replace('@', '_at_')}.png"
    qr_path = os.path.join(qr_folder, qr_filename)
    img.save(qr_path)

    # Return path for use in HTML
    return f"/static/qr/{qr_filename}"
