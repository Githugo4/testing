"""
    Email Notification Utility
"""
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib
from jinja2 import Environment
import codecs
from email.mime.base import MIMEBase
from email import encoders
import os


class EmailNotification(object):
    """
    This is used to handle email notification
    """

    def __init__(self, smtp_host, smtp_port, smtp_authentication_enabled):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_authentication_enabled = smtp_authentication_enabled

    def send_mail(self,sender, sender_password, email_alias_name, recipients, subject, template, dynamic_contents,
                  attachment, file_name, file_path, image_available=False, image_path=""):

        """
        sends email based on dynamic template
        :param sender: sender email id
        :param sender_password: sender password
        :param recipients: comma seperated list of recipients email ids
        :param subject: email subject
        :param template: template file path
        :param dynamic_contents: dictionary containing keys in template with values
        :return:
        """
        try:
            commaspace = ', '
            # Create the enclosing (outer) message
            themsg = MIMEMultipart()
            themsg['Subject'] = subject
            themsg['To'] = commaspace.join(recipients)
            themsg['From'] = email_alias_name or sender
            themsg.preamble = 'You will not see this in a MIME-aware mail reader.\n'

            template = codecs.open(template)
            template = template.read()
            # render the corresponding template and substitute values in the body dynamically
            msg_text = MIMEText(
                Environment(autoescape=True).from_string(template).render(dynamic_contents=dynamic_contents), "html")
            # Add the attachments to the message
            themsg.attach(msg_text)

            if image_available:
                # This example assumes the image is in the current directory
                fp = open(image_path, 'rb')
                msg_image = MIMEImage(fp.read())
                fp.close()

                # Define the image's ID as referenced above
                msg_image.add_header('Content-ID', '<image>')
                themsg.attach(msg_image)

            if attachment:
                attachment = open(
                    file_path
                    , "rb")
                # instance of MIMEBase and named as p
                p = MIMEBase('application', 'octet-stream')

                # To change the payload into encoded form
                p.set_payload((attachment).read())

                # encode into base64
                encoders.encode_base64(p)

                p.add_header('Content-Disposition', "attachment; filename= %s" % file_name)

                # attach the instance 'p' to instance 'msg'
                themsg.attach(p)

            composed = themsg.as_string()

            # Send the email
            s = smtplib.SMTP(self.smtp_host, self.smtp_port)
            if self.smtp_authentication_enabled:

                s.ehlo()
                s.starttls()
                s.login(sender, sender_password)
            s.sendmail(sender, recipients, composed)
            s.quit()
        except Exception as ex:
            raise Exception(str(ex))

