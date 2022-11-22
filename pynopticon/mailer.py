import sendgrid
import sendgrid.helpers.mail


def send_email(sg, to_emails, from_email, subject, text):
  from_email = sendgrid.helpers.mail.Email(from_email)
  to_email = [sendgrid.helpers.mail.To(to) for to in to_emails]
  content = sendgrid.helpers.mail.Content("text/plain", text)
  mail = sendgrid.helpers.mail.Mail(from_email, to_email, subject, content)
  response = sg.client.mail.send.post(request_body=mail.get())

  if response.status_code not in range(200, 203):
    print("Error sending email")
    print(response.status_code)
