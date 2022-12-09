from __future__ import print_function
from io import BytesIO
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from PIL import Image
import socket
import string
import random
import os 
import subprocess
import requests
import time
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint

def sendMail(sender,receivers,object_mail, msgTxt, img=None):
    port = 25 
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = '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'
    msg = MIMEMultipart()
    msg['Subject'] = object_mail
    msg['From'] = sender
    msg['To'] = ', '.join(receivers)

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    subject = object_mail
    sender = {"name":"Raspberry Pi project","email":'raspberry@project.g3s3'}
    to = [{"email":'chadow.video@gmail.com',"name":"Julien SANCHEZ"}]
    reply_to = {"email":"raspberry@project.g3s3","name":"NO REPLY"}
    headers = {"Some-Custom-Name":"unique-id-1234"}
    params = {"parameter":"My param value","subject":object_mail}

    if not img is None:
        im=Image.fromarray(img, 'RGB')
        memf = BytesIO()
        im.save(memf, "JPEG")
        image = MIMEImage(memf.getvalue(), name="attachement.jpg")
        if not "\n" in msgTxt:
            n=5
            name=''.join(random.choices(string.ascii_uppercase + string.digits, k=n))+".jpg"
            while os.path.isfile('images/'+name):
                name=''.join(random.choices(string.ascii_uppercase + string.digits, k=n))+".jpg"
                n+=1
            local_ip = subprocess.run(['hostname', '-I'], stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n', '').replace(' ', '')
            msgTxt+="\nThe system do not know him. Do you want to add him to your database ? \nhttp://"+str(local_ip)+"/add?file="+name
            msgTxt+="\nYou should be on the same local network than the pi."
            im.save("images/"+name, "JPEG")
            print("Save image at : images/"+name)
        msg.attach(image)
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, reply_to=reply_to, headers=headers, html_content=msgTxt, sender=sender, subject=subject)
    else:
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, reply_to=reply_to, headers=headers, html_content=msgTxt, sender=sender, subject=subject)

    
    msg.attach(MIMEText(msgTxt))
    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
    with smtplib.SMTP('localhost', port) as server:
        try:
            return server.sendmail(sender, receivers, msg.as_string())
        except:
            print("Error while sending the email with local smtp server")

def sendEmailAlert(msg, ImgFileName=None, name=None):
    if name!=None:
        msg+="\nThe system already know this person : "+str(name)

    return sendMail('raspberry@project.g3s3',
        ['julien.sanchez74@orange.fr','chadow.video@gmail.com','julien.sanchez@univ-lyon1.fr'],
        "New Camera Detection",msg, ImgFileName)


