from app import celery_app, generate_embeddings


######################################################################
# No need to define tasks here as they are already defined in app.py
######################################################################


# import smtplib
# import os
# from dotenv import load_dotenv
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText


# load_dotenv()
# smtp_pass = os.getenv("SMTP_PASS")




# def generate_email(subject, message, user_name):
#     content = f"""
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Congratulations!</title>
#     <style>
#         body {{
#             font-family: Arial, sans-serif;
#             background-color: #f5f5f5;
#             margin: 0;
#             padding: 0;
#             text-align: center;
#         }}
#         .container {{
#             max-width: 600px;
#             margin: 50px auto;
#             background-color: #ffffff;
#             padding: 20px;
#             border-radius: 10px;
#             box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
#         }}
#         h1 {{
#             color: #333333;
#         }}
#         p {{
#             color: #666666;
#             line-height: 1.6;
#             margin-bottom: 20px;
#         }}
#         table {{
#             width: 100%;
#             border-collapse: collapse;
#         }}
#         table, th, td {{
#             border: 1px solid #dddddd;
#         }}
#         th, td {{
#             padding: 8px;
#             text-align: left;
#         }}
#         th {{
#             background-color: #f2f2f2;
#         }}
#         .button {{
#             display: inline-block;
#             background-color: #4CAF50;
#             color: #ffffff;
#             padding: 10px 20px;
#             text-decoration: none;
#             border-radius: 5px;
#             transition: background-color 0.3s ease;
#         }}
#         .button:hover {{
#             background-color: #45a049;
#         }}
#     </style>
# </head>
# <body>
#     <div class="container">
#         <h1>Congratulations! {user_name}</h1>
#         <p>{subject}</p>
#         <p>{message}</p>
#         <p>Keep up the great work!</p>
#         <a href="#" class="button">Learn More</a>
#     </div>
# </body>
# </html>
# """
#     return content

# def send_alert_email(subject, receiver, user_name, message):
#     try:
#         msg = MIMEMultipart()
#         msg['Subject'] = subject
#         msg['From'] = 'freshcart.appv2@gmail.com'
#         msg['To'] = receiver

#         msg.attach(MIMEText(generate_email(subject, message, user_name), 'html'))

#         smtp_server = 'smtp.gmail.com'
#         port = 587
#         smtp_user = 'freshcart.appv2@gmail.com'
#         # smtp_pass = 'COMMENTincommentjkfjekxtbkefaw' 

#         with smtplib.SMTP(smtp_server, port) as server:
#             server.starttls()
#             server.login(smtp_user, smtp_pass)
#             server.sendmail(smtp_user, receiver, msg.as_string())
#         print("Successfully sent the message!")
#     except smtplib.SMTPException as e:
#         print(f"SMTP error occurred: {e}")
#     except Exception as e:
#         print(f"An error occurred: {e}")

# send_alert_email(
#     "sample subject",
#     "surajnish02@gmail.com",
#     "rajnish",
#     "test message"
# )
