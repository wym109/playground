import requests
import time
while(True):
    try:
        response =requests.get('https://api.impfstoff.link/?v=0.3')
        print(response.content)
        if str(response.content).find('"open":true') != -1:
            print('ALARM\a')
        else:
            print('still nothing')
    except e:
        print(f"Exception: {e}")
    time.sleep(0.5)


# from email.message import EmailMessage
# msg = EmailMessage()
# msg.set_content(url)
# msg['From'] = '..@..'
# msg['To'] = '..@..'
# msg['Subject'] = 'Appointment'
# fromaddr = '..@..'
# toaddrs = [..@..]
# server = smtplib.SMTP('', 587) #your server
# server.starttls()
# server = smtplib.SMTP_SSL('', 465) #your server
# server.login() #username and password
# server.send_message(msg)
# server.quit()