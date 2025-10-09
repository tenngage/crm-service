import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from src.tasks.celery_app import app

@app.task(bind=True, max_retries=3, default_retry_delay=60)
def send_email(self, user_email: str, username: str):
    try:
        smtp_config = {
            "server": "smtp.gmail.com",
            "port": 587,
            "email": "ibi0880@gmail.com",
            "password": "zrgr zqtb uhsf aidi",
        } 
        message = MIMEMultipart("alternative")
        message["Subject"] = f"Добро пожаловать в CRM, {username}! 🚀"
        message["From"] = smtp_config["email"]
        message["To"] = user_email
        # HTML шаблон письма
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; }}
                .container {{ max-width: 600px; margin: 0 auto; background: #f9f9f9; padding: 30px; }}
                .header {{ background: #4F46E5; color: white; padding: 20px; text-align: center; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Добро пожаловать! 🎉</h1>
                </div>
                <div style="padding: 20px;">
                    <h2>Привет, {username}!</h2>
                    <p>Спасибо за регистрацию в нашем CRM для фрилансеров.</p>
                    <p>Теперь вы можете:</p>
                    <ul>
                        <li>Создавать и управлять проектами</li>
                        <li>Отслеживать задачи и время</li>
                        <li>Вести учет клиентов и платежей</li>
                    </ul>
                    <p>Если у вас есть вопросы, просто ответьте на это письмо!</p>
                    <br>
                    <p>С уважением,<br>Команда FreelanceCRM</p>
                </div>
            </div>
        </body>
        </html>
        """
            
        # Прикрепляем HTML версию
        message.attach(MIMEText(html_content, "html"))
            
        # Отправляем письмо
        with smtplib.SMTP(smtp_config["server"], smtp_config["port"]) as server:
            server.starttls()
            server.login(smtp_config["email"], smtp_config["password"])
            server.send_message(message)

            return {
                "status": "success",
                "email": user_email,
            }

    except smtplib.SMTPAuthenticationError as e:
        return {
            "status": "error",
            "error": "SMTP authentication failed"
        }