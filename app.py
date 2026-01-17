from flask import Flask, render_template, request, redirect, url_for, session, send_file
import os
from werkzeug.utils import secure_filename
import paramiko
import qrcode

app = Flask(__name__)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = 'uploads'
QR_FOLDER = 'static/qr'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(QR_FOLDER, exist_ok=True)

# Simple in-memory user store
users = {}

def send_file_sftp(local_path, remote_path, hostname, port, username, password):
    try:
        transport = paramiko.Transport((hostname, port))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put(local_path, remote_path)
        sftp.close()
        transport.close()
        return True
    except Exception as e:
        print(f"SFTP Error: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if "@gmail.com" in email or "@yahoo.com" in email or "@outlook.com" in email:
            users[email] = password
            session['email'] = email
            return redirect(url_for('home'))
        else:
            return "Only Google, Yahoo, or Microsoft accounts are allowed!"
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users and users[email] == password:
            session['email'] = email
            return redirect(url_for('home'))
        else:
            return "Invalid credentials. Try again!"
    return render_template('login.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'email' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'files' not in request.files:
            return "No files part"
        files_to_upload = request.files.getlist('files')

        # SFTP test server config (for demo only)
        hostname = 'test.rebex.net'
        port = 22
        username = 'demo'
        password = 'password'
        remote_base_path = '/pub/example/'

        for file in files_to_upload:
            if file.filename != '':
                filename = secure_filename(file.filename)
                local_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(local_path)

                remote_path = os.path.join(remote_base_path, filename)
                success = send_file_sftp(local_path, remote_path, hostname, port, username, password)

                if success:
                    return redirect(url_for('generate_qr', filename=filename))
                else:
                    return f"Failed to send {filename} via SFTP."

    return render_template('home.html', email=session['email'])

@app.route('/generate_qr/<filename>')
def generate_qr(filename):
    file_url = f"sftp://demo:test.rebex.net/pub/example/{filename}"
    img = qrcode.make(file_url)
    qr_path = os.path.join(QR_FOLDER, f"{filename}.png")
    img.save(qr_path)
    return render_template('show_qr.html', qr_image=f"/{qr_path}")

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5002)
