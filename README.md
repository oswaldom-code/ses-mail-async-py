# ses-mail-async-py

This Python program utilizes the Amazon Simple Email Service (SES) to send emails with attachments to a list of recipients in parallel. It is designed to handle a specified rate limit to comply with SES restrictions.

## Prerequisites

Before running the program, ensure that you have set the following environment variables:

- `AWS_ACCESS_KEY_ID`: Your AWS Access Key ID.
- `AWS_SECRET_ACCESS_KEY`: Your AWS Secret Access Key.
- `REGION_NAME`: The AWS region where SES is configured.

## Usage

1. Clone the repository:

   ```bash
   git clone git@github.com:oswaldom-code/ses-mail-async-py.git
   cd ses-mail-async-py
   ```

2. Install the required Python packages:

   ```bash
   pip install boto3
   ```

3. Create a folder named `attachments` in the same directory as the script and place the files you want to attach inside it.

4. Create a file named `email_list.txt` containing the list of recipient emails, with each email on a new line.

5. Create an HTML file named `email_content.html` containing the email content in HTML format.

6. Run the script:

   ```bash
   python ses-mail-async.py
   ```

The program will send emails to the specified recipients with the provided HTML content and attached files.

## Rate Limit

The program respects the SES rate limit by sending emails at a specified rate (11 emails per second by default) using a ThreadPoolExecutor.

## Handling Failures

Failed emails (if any) will be logged in a file named `failed_emails.txt` for further investigation.

Feel free to customize the program to meet your specific needs.
