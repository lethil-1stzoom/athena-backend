from django.conf import settings
from mailjet_rest import Client
from django.template.loader import get_template


MAILJET_API_KEY = settings.MAILJET_API_KEY
MAILJET_SECRET_KEY = settings.MAILJET_SECRET_KEY

def send_email(email, name, subject, by):
    html = get_template('Email/notify.html')
    context = {'name': name, 'by': by}
    body = html.render(context)
    mailjet = Client(auth=(MAILJET_API_KEY, MAILJET_SECRET_KEY), version='v3.1')
    data = {
        'Messages':[
            {
                "From":{
                    "Email": "lethil@1stzoom.com",
                    "Name": "Athena Service"
                },
                "To": [
					{
						"Email": email,
						"Name": name
					}
				],
                "Subject": subject,
                "HTMLPart": body
            }
        ]
    }
    result = mailjet.send.create(data=data)
    return result.status_code
