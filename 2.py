from Google import Create_Service
import os
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import mimetypes
 
CLIENT_SECRET_FILE = '<Client Secret File'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']
 
service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
 
file_attachments = ['<Attachment 1>', '<Attachment 2>', '<Attachment n>']
 
emailMsg = 'Three files attached'
 
# create email message
mimeMessage = MIMEMultipart()
mimeMessage['to'] = 'email1@EmailDomain.com; email2@EmailDomain.com'
mimeMessage['subject'] = 'You got files'
mimeMessage.attach(MIMEText(emailMsg, 'plain'))
 
# Attach files
for attachment in file_attachments:
    content_type, encoding = mimetypes.guess_type(attachment)
    main_type, sub_type = content_type.split('/', 1)
    file_name = os.path.basename(attachment)
 
    f = open(attachment, 'rb')
 
    myFile = MIMEBase(main_type, sub_type)
    myFile.set_payload(f.read())
    myFile.add_header('Content-Disposition', 'attachment', filename=file_name)
    encoders.encode_base64(myFile)
 
    f.close()
 
    mimeMessage.attach(myFile)
 
raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
 
message = service.users().messages().send(
    userId='me',
    body={'raw': raw_string}).execute()
 
print(message)