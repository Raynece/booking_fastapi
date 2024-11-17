import smtplib
from pathlib import Path

from PIL import Image
from pydantic import EmailStr

from app.tasks.celery_app import celery_app
from app.tasks.email_templates import create_booking_confirmation_template


@celery_app.task
def process_pic(
        path:str,
):
    im_path = Path(path)
    im = Image.open(im_path)
    im_resized_1000_500 = im.resize((1000,500))
    im_resized_200_100 = im.resize((200, 100))
    im_resized_1000_500.save(f'app/static/images/resized_1000_500_{im_path.name}')
    im_resized_200_100.save(f'app/static/images/resized_200_100_{im_path.name}')

@celery_app.task
def send_booking_confirmation_email(
        booking:dict,
        email_to: EmailStr,
):
    email_to_mock = 'filkuz19@gmail.com'
    msg_content = create_booking_confirmation_template(booking,email_to_mock)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login('filkuz19@gmail.com','zqdj sxfe orxd zgct')
        server.send_message(msg_content)