from email.mime import application
import smtplib
import imghdr
from email.message import EmailMessage

contacts = ["shiyani.avinash8489@gmail.com", ]


msg = EmailMessage()
msg["Subject"] = "Subject"
msg["From"] = "ks4223839@gmail.com"
msg["To"] = "shiyani.avinash8489@gmail.com"
# msg["To"] = ", ".join(contacts)
msg.set_content("Test body")

# Image
# files = ["download.png"]

# for file in files:
#     with open("download.png", "rb") as f:
#         file_data = f.read()
#         file_type = imghdr.what(f.name)
#         file_name = f.name

#     msg .add_attachment(file_data, maintype="image",
#                         subtype=file_type, filename=file_name)


# files = ["FastAPI Documents.docx"]

# for file in files:
#     with open(file, "rb") as f:
#         file_data = f.read()
#         # file_type = imghdr.what(f.name)
#         file_name = f.name

#     msg .add_attachment(file_data, maintype="application",
#                         subtype="octet-stream", filename=file_name)


# with smtplib.SMTP_SSL(host="smtp.gmail.com", port=465) as smtp:

#     smtp.login("ks4223839@gmail.com", "@Admin123")

#     smtp.send_message(msg=msg)

# msg.set_content("Hello html ")

# msg.add_alternative("""\
# <!DOCTYPE html>
# <html>
#     <body>
#         <h1 style="color:SlateGray;">This is an HTML Email!</h1>
#     </body>
# </html>
# """, subtype="html")

# with smtplib.SMTP_SSL(host="smtp.gmail.com", port=465) as smtp:

#     smtp.login("ks4223839@gmail.com", "@Admin123")

#     smtp.send_message(msg=msg)
