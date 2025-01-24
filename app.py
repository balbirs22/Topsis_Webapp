from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
import pandas as pd
import os
import secrets
from topsis import topsis  # Make sure this is properly set up and imported

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.secret_key = secrets.token_hex(24)

def create_upload_folder():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

create_upload_folder()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        weights = request.form['weights']
        impacts = request.form['impacts']
        file = request.files['file']

        print("Email:", email)  # Debugging
        print("Weights:", weights)  # Debugging
        print("Impacts:", impacts)  # Debugging
        print("File Received:", file.filename)  # Debugging

        if file and file.filename != '':
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            print(f"File saved to {filepath}")  # Debugging

            try:
                data = pd.read_csv(filepath)
                results = topsis(data, weights, impacts)
                result_path = os.path.join(app.config['UPLOAD_FOLDER'], 'results.csv')
                results.to_csv(result_path, index=False)
                # send_email(email, result_path)  # Temporarily commenting out to focus on file upload
                flash('File uploaded and processed successfully!', 'success')
            except Exception as e:
                flash(f"Processing Error: {str(e)}", 'error')
            finally:
                os.remove(filepath)  # Clean up file after processing
        else:
            flash('No file uploaded or file is empty.', 'error')
        return redirect(url_for('index'))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
