import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text      import MIMEText

class Email:
    """ email sending methods
        - plain
        - as html """



    def __init__(self):
        self.deliveryFailures = 0



    def sendEmail(self, TO, text, s_onFailure='username@domain.com'):
        HOST = 'smtp.domain.com'
        FROM = 'username@domain.com'
        server = smtplib.SMTP(HOST)
        msg = '''From: username@domain.com
Subject: Update
'''
        recipient = 'To:' + TO
        msg = recipient + msg + text
        try:
            server.sendmail(FROM, TO, msg)
        except Exception as e:
            self.deliveryFailures += 1
            server.sendmail('jjap@domain.com',
                            s_onFailure,
                            '''From: Jens Jap
To: %s
Subject: Update
eMail delivery failure: %s
Error Message: %s''' % (TO, TO, str(e)))
        finally:
            server.quit()
        


    def sendEmail_html(self, TO, html, s_onFailure='jjap@domain.com'):
        # me == my email address
        # TO == recipient's email address
        me = "username@domain.com"

        # Create message container - the correct MIME type is
        # multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Update"
        msg['From'] = me
        msg['To'] = TO

        # Create the body of the message (a plain-text and an HTML version).
        text = """The following email is to report on the results of today's\n
update on the iSeries\nSince you are reading this message, it means
that your browser or mail client is unable to process the html message. Please
find a client that can view html to properly display the content of this email\n

sincerely,
Jens Jap
"""

        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message,
        # in this case the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)

        # Send the message via local SMTP server.
        server = smtplib.SMTP('smtp.domain.com')
        # sendmail function takes 3 arguments: sender's address, recipient's
        # address and message to send - here it is sent as one string.
        try:
            server.sendmail(me, TO, msg.as_string())
        except Exception as e:
            self.deliveryFailures += 1
            server.sendmail('jjap@domain.com',
                            s_onFailure,
                            '''From: Jens Jap
To: %s
Subject: Report Summary
eMail delivery failure: %s
Error Message: %s''' % (TO, TO, str(e)))
        finally:
            server.quit()
