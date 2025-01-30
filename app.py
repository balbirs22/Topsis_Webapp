from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
import pandas as pd
import os
import secrets
from flask_mail import Mail, Message
from topsis import topsis  # Ensure this is properly set up and imported

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.secret_key = secrets.token_hex(24)

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'balbirs2204@gmail.com'
app.config['MAIL_PASSWORD'] = 'txgwsmpafthcdpru'  # Ensure this is your App Password
mail = Mail(app)

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

        if file and file.filename != '':
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            try:
                data = pd.read_csv(filepath)
                results = topsis(data, weights, impacts)
                result_path = os.path.join(app.config['UPLOAD_FOLDER'], 'results.csv')
                results.to_csv(result_path, index=False)

                # Send email with results
                msg = Message("TOPSIS Analysis Result", 
                              sender=app.config['MAIL_USERNAME'], 
                              recipients=[email])
                msg.body = "Please find attached the results of your TOPSIS analysis."
                with app.open_resource(result_path) as fp:
                    msg.attach("results.csv", "text/csv", fp.read())
                mail.send(msg)

                flash('File uploaded and results emailed successfully!', 'success')
            except Exception as e:
                flash(f"Processing Error: {str(e)}", 'error')
                app.logger.error('Error sending email: %s', str(e))  # Log the error for debugging
            finally:
                os.remove(filepath)  # Clean up file after processing
        else:
            flash('No file uploaded or file is empty.', 'error')
        return redirect(url_for('index'))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
