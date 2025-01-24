import smtplib
from email.mime.text import MIMEText

# SMTP setup
smtp_server = 'smtp.gmail.com'
smtp_port = 587
username = 'balbirs2204@gmail.com'
password = 'npbrkbhsryrargph'  # Use app password if 2FA is enabled

# Email content
msg = MIMEText('This is a test email from Gmail SMTP via Python.')
msg['Subject'] = 'Test Email'
msg['From'] = username
msg['To'] = 'balbirs2204@gmail.com'

try:
    # Connect and send email
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(username, password)
    server.sendmail(username, ['balbirs2204@gmail.com'], msg.as_string())
    server.quit()
    print("Email sent successfully!")
except Exception as e:
    print("Failed to send email:", e)
