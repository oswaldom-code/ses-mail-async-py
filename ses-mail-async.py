import os
import time
import boto3
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from concurrent.futures import ThreadPoolExecutor

# Set up AWS credentials and region
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
region_name = os.environ.get('REGION_NAME')

# Set up the folder path for attachments
attachments_folder_path = './attachments'

# Create an SES client
ses_client = boto3.client('ses',
                          aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key,
                          region_name=region_name)

# attach_files_from_folder function to attach files from a folder
def attach_files_from_folder(msg, folder_path):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as f:
                part = MIMEApplication(f.read(), Name=os.path.basename(file_path))
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                msg.attach(part)

# send_email_with_attachments function to send an email with attachments
def send_email_with_attachments(recipient, subject, html_content, folder_path):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = 'no-reply@domain.com'
    msg['To'] = recipient

    # Attach HTML content
    msg.attach(MIMEText(html_content, 'html'))

    # Attach files from folder if it exists
    attach_files_from_folder(msg, folder_path)

    try:
        response = ses_client.send_raw_email(
            Source=msg['From'],
            Destinations=[recipient],
            RawMessage={'Data': msg.as_string()}
        )
        return response
    except ClientError as e:
        print(f"Error try to send email to {recipient}: {e}")
        return None



# Read email list and email content from files
with open('email.list.txt', 'r') as emails_file, open('email_content.html', 'r', encoding='utf-8') as html_file:
    email_list = emails_file.read().splitlines()
    email_content = html_file.read()

# Set up the rate limit for sending emails
rate_limit = 11  # 11 emails per second (SES limit is 14 per second)
failed_emails = []

# send_emails_parallel function to send emails in parallel
def send_emails_parallel(email):
    global i
    response = send_email_with_attachments(
        email,
        "Subject of the email",
        email_content, attachments_folder_path)
    if not response:
        failed_emails.append(email)
    print(f"Email {i} sent to {email}")
    i += 1

# counter for emails
i = 1
# start time for rate limit
start_time = time.time()

# ThreadPoolExecutor to send emails in parallel with a rate limit 
with ThreadPoolExecutor(max_workers=11) as executor:
    for email in email_list:
        executor.submit(send_emails_parallel, email)
        
        # Calculate elapsed time and sleep if necessary
        elapsed_time = time.time() - start_time
        if elapsed_time < i / rate_limit:
            time.sleep((i / rate_limit) - elapsed_time)

# Write failed emails to a file
with open('failed_emails.txt', 'w') as failed_file:
    for email in failed_emails:
        failed_file.write(f"{email}\n")

print(f"Total emails sent: {i-1}")
