#coding=utf-8 
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def SendEmail(receiver,subject,text):
    try:
        sender = 'kuang.brian@51onion.com'
        smtpserver = 'smtp.exmail.qq.com'
        user = 'kuang.brian@51onion.com'
        password = 'Kaq130109'
        
        msg = MIMEText(_text=text,_charset='utf-8')
        msg['Subject'] = Header(subject,charset='utf-8')
        msg['From'] = sender
        msg['To'] = receiver
        
        
        smtp = smtplib.SMTP(smtpserver)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.set_debuglevel(1)
        smtp.login(user, password)
        smtp.sendmail(sender, [receiver], msg.as_string())
        smtp.quit()
        return True
    except Exception as e:
        print (e)
        return False