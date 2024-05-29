from uagents import Agent, Context,Model
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

smtp_pass = os.getenv("SMTP_PASS")
myagent = Agent(name ="myagent",
              seed="ahgsuasuishwhwryuqioqbsjqjwoqskxsoxw",
              port=8001,
              endpoint=["http://127.0.0.1:8001/submit"]
              )

class AgentRequest(Model):
    name : str
    email: str
    chatbot_name: str

class AgentResponse(Model):
    message : str

class ErrorMessage(Model):
    err_msg : str

async def query_analysis(msg):
    print(msg.name, msg.email, msg.chatbot_name)
    print('\n'*5)
    send_alert_email("ChatBot ready to explore", msg.email, msg.name, msg.chatbot_name)
    return "Successfully sent the email"


@myagent.on_event("startup")
async def say_hello(ctx:Context):
    ctx.logger.info(f'Hello, my adress is {ctx.address}' )

@myagent.on_query(model=AgentRequest,replies={AgentResponse})
async def query_handler(ctx:Context,sender : str, msg :AgentRequest):
    try:
        ctx.logger.info(f'Fetching details of {msg.email}')
        response = await query_analysis(msg)
        ctx.logger.info(response)
        await ctx.send(sender,message=AgentResponse(message=response))
    except Exception as E :
        err_msg='Error in sending the email'
        ctx.logger.info(err_msg)
        await ctx.send(sender,message=ErrorMessage(err_msg='Error in sending the email'))


# ===================================== email =============================================================
def send_alert_email(subject, receiver, user_name, chatbot_name):
    try:
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = 'freshcart.appv2@gmail.com'
        msg['To'] = receiver

        msg.attach(MIMEText(generate_email(subject, chatbot_name, user_name), 'html'))

        smtp_server = 'smtp.gmail.com'
        port = 587
        smtp_user = 'freshcart.appv2@gmail.com'

        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, receiver, msg.as_string())
        print("Successfully sent the message!")
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")



def generate_email(subject, chatbot_name, user_name):
    content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Congratulations!</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            margin: 0;
            padding: 0;
            text-align: center;
        }}
        .container {{
            max-width: 600px;
            margin: 50px auto;
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }}
        h1 {{
            color: #333333;
        }}
        p {{
            color: #666666;
            line-height: 1.6;
            margin-bottom: 20px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        table, th, td {{
            border: 1px solid #dddddd;
        }}
        th, td {{
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
        }}
        .button {{
            display: inline-block;
            background-color: #4CAF50;
            color: #ffffff;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 5px;
            transition: background-color 0.3s ease;
        }}
        .button:hover {{
            background-color: #45a049;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Congratulations! {user_name}</h1>
        <p>Your {chatbot_name} chatbot is ready!</p>
        <a href="http://localhost:3000/bot/{chatbot_name}" class="cta-button">Go to My Chatbots</a>
    </div>
</body>
</html>
"""
    return content



if __name__ == "__main__":
    print("Hello")
    myagent.run()

