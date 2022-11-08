from django.core.mail import send_mail
from django.template.loader import render_to_string

from django.conf import settings


def create_verify_email(user, recipient_list):
    # frontend_link = settings.FRONT_END_URL

    # use tmp url
    link = settings.FRONT_END_URL + '/api/user/email/verify?token='

    token = user.token

    link_verify = link + token

    msg_html = render_to_string(
        'api/hello.html', {'link': link_verify})

    send_mail(
        subject='Verify email',
        message='',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list,
        html_message=msg_html,
    )
