from email.message import EmailMessage
import ssl
import smtplib
from sshhhh import EMAIL_ADDRESS, EMAIL_PASSWORD
from validate_email import validate_email


def isValid(email: str) -> bool:
    """
        Validates whether the given email address is valid or not.

    """
    return validate_email(email_address=email)


def send_email(receiver, subject, body) -> bool:
    """
    Sends an email message.
    Returns:

    Parameters:
    receiver (str): The email address of the recipient.
    subject (str): The subject of the email.
    body (str): The body content of the email.

        bool: True if the email is sent successfully, False otherwise.
    """
    # email_sender = EMAIL_ADDRESS
    # email_password = EMAIL_PASSWORD
    # email_receiver = receiver

    em = EmailMessage()
    em["From"] = EMAIL_ADDRESS
    em['To'] = receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.sendmail(EMAIL_ADDRESS, receiver, em.as_string())
            return True
    except:
        return False
