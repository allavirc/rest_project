from django.core.mail import send_mail

def send(user_email: str):
    try:
        send_mail(
            'Вы cохранены в базе',
            'Теперь вы в ней навсегда',
            ['allavirc2@gmail.com'],
            [user_email],
            fail_silently=False
        )
    except Exception as e:
        print(e)