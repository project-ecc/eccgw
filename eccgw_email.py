import smtplib
import ssl

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import settings

################################################################################

def sendEmail(address = '', text = ''):

    message = MIMEMultipart("alternative")

    message["Subject"] = "ECC Message"
    message["From"]    = settings.send_email
    message["To"]      = address

    html = """\
    <html>
      <body>
        <p>%s</p>
      </body>
    </html>
    """ % text

    message.attach(MIMEText(text, "plain"))
    message.attach(MIMEText(html, "html"))

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(settings.smtp_server, settings.smtp_port, context=context) as server:
        server.login(settings.email_address, settings.email_pass)
        server.sendmail(settings.send_email, address, message.as_string())
        server.quit()