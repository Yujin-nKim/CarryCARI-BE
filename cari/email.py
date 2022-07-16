from pathlib import Path
from email.mime.image import MIMEImage
from django.core.mail import EmailMultiAlternatives

recipient = "recipient_email" #수신자
sender = "sender_email" #전송자
image_path = '_media/result_images/00.jpg' #이미지경로
image_name = Path(image_path).name #이미지 이름
subject = "View your generated caricature!." #주제
html_message = f"""
<!doctype html>
    <html lang=en>
        <head>
            <meta charset=utf-8>
            <title>Some title.</title>
        </head>
        <body>
            <h1>{subject}</h1>
            <p>
            Here is the generated caricature. Thank you! <br>
            <img src='cid:{image_name}'/>
            </p>
        </body>
    </html>
"""

# the function for sending an email
def send_email(subject, text_content, html_content=None, sender=sender,
               recipient=recipient, image_path=None, image_name=None):

    email = EmailMultiAlternatives(subject=subject, body=text_content,
                                   from_email=sender, to=recipient if isinstance(recipient, list) else [recipient])

    if all([html_content,image_path,image_name]):
        email.attach_alternative(html_content, "text/html")
        email.content_subtype = 'html'  # set the primary content to be text/html
        email.mixed_subtype = 'related' # it is an important part that ensures embedding of an image

        with open(image_path, mode='rb') as f:
            image = MIMEImage(f.read())
            email.attach(image)
            image.add_header('Content-ID', f"<{image_name}>")

    email.send()
