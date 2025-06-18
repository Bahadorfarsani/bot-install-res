import os
from flask import Flask, send_from_directory, url_for



app = Flask(__name__)

YOUR_DOMAIN = 'arm.freebfanet.de'

def get_files_in_directory(directory):
    return [file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]

@app.route('/')
def index():
    return "Access denied. Please specify a filename in the URL."

@app.route('/<filename>')
def serve_file(filename):
    files = get_files_in_directory('./accounts')
    if filename in files:
        return send_from_directory('./accounts', filename, as_attachment=True)
    else:
        return f"File '{filename}' not found."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
