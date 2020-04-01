import smtplib
import ssl

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

################################################################################

def sendEmail(address = '', content = ''):

    smtp_server   = "smtp.gmail.com"
    smtp_port     = 465 # For SSL
    username      = "eccoin42"
    password      = "ecc_IsAVeryNiceCoin123!"
    email_address = "eccoin42@gmail.com"

    send_email    = "noreply@eccoin.bit"
    recv_email    = address

    message = MIMEMultipart("alternative")

    message["Subject"] = "ECC Message"
    message["From"]    = send_email
    message["To"]      = recv_email

    text = content

    html = """\
    <html>
      <body>
        <p>%s</p>
      </body>
    </html>
    """ % content

    message.attach(MIMEText(text, "plain"))
    message.attach(MIMEText(html, "html"))

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
        server.login(email_address, password)
        server.sendmail(send_email, recv_email, message.as_string())
        server.quit()