#Import python library 
import RPi.GPIO as GPIO #to control and interact with the GPIO pins
import datetime as dt #manage datetime
import time #manage time
import smtplib #necessary to send email
import blynklib #Cononection with blynk app
import boto3 #Connection to aws 

from time import sleep
from sys import exit
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


#Get data from HC-SR04 Sensor
def distance():
    try:
          GPIO.setwarnings(False) #Disable eventually warnings
          GPIO.setmode(GPIO.BOARD) #Set GPIO mode to GPIO.BOARD - to use physical pin numbers

          PIN_TRIGGER = 7 #set number of trigger pin
          PIN_ECHO = 11 #set number of echo pin

          GPIO.setup(PIN_TRIGGER, GPIO.OUT) #Set trigger pin as output - Necessary to pings this pin and start sensor
          GPIO.setup(PIN_ECHO, GPIO.IN) #Set echo pin as input 

          GPIO.output(PIN_TRIGGER, GPIO.LOW) #set trigger pin to low 

          #print("Waiting for sensor to settle")

          time.sleep(3) #sleep the script for 0.1 seconds

          #print("Calculating distance")

          GPIO.output(PIN_TRIGGER, GPIO.HIGH) #set trigger pin to low 

          time.sleep(0.00001) #sleep the script for 1 nanoseconds - distance sensor requires a pulse of 1 nanosecond to trigger it

          GPIO.output(PIN_TRIGGER, GPIO.LOW) #set trigger pin to low 

          while GPIO.input(PIN_ECHO)==0:  #while loop to check if PIN_ECHO is 0
                pulse_start_time = time.time()  #assign value to pulse_start_time
          while GPIO.input(PIN_ECHO)==1:  #while loop to check if PIN_ECHO is 1
                pulse_end_time = time.time() #assign value to pulse_end_time

          pulse_duration = pulse_end_time - pulse_start_time  #assign value to pulse_duration
          distance = round(pulse_duration * 17150, 2) #get distance value
          date = dt.datetime.now().strftime('%d-%m-%Y %H:%M:%S') #get current timestamp
          return round(distance,2),date #return distance and timestamp value
    except:
        print('An error occured during distance calculation')
    finally:
          GPIO.cleanup() #cleanup on GPIO

#Send email function
def send_email(subject,message):
    email = 'testappdeveloper@yahoo.com'
    password = 'fekagfmzwerkqjxl'
    send_to_email = 'antonyoabate94@gmail.com'

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = send_to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('smtp.mail.yahoo.com', 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string() 
    server.sendmail(email, send_to_email, text)
    server.quit()


#Calculate percentage 
def percentage(part, whole):
  return int(round(100 * float(part)/float(whole)))

#Send data to Blynk app 
def blynk_send_data(date,distance,percentage,level):
            BLYNK_AUTH = '16033f23f33648dd9c5323d2751da438'
            blynk = blynklib.Blynk(BLYNK_AUTH)
            blynk.run()
            blynk.virtual_write(0,date)
            blynk.virtual_write(1,dist)
            blynk.virtual_write(2,perc)
            blynk.virtual_write(3,level)
            
def ec2_start_instance():
    ec2 = boto3.client('ec2',region_name='us-east-1')
    print('Starting ec2 instance...')
    instance = ec2.start_instances(InstanceIds=["i-0e17ad1f5d932c99f"])
    sleep(60)
    print('Instance successfully started')
    
def ec2_stop_instance():
    ec2 = boto3.client('ec2',region_name='us-east-1')
    print('Stopping ec2 instance...')
    instance = ec2.stop_instances(InstanceIds=["i-0e17ad1f5d932c99f"])
    sleep(60)
    print('Instance successfully stopped')
            
#Get public DNS name of ec2 Instance
def ec2_get_dns_name():
    ec2 = boto3.resource('ec2',region_name='us-east-1')
    instance = ec2.Instance('i-0e17ad1f5d932c99f')
    if instance.state['Name'] == 'running':
        instance_subject ='Water Level Monitoring Avaible' 
        instance_message = "The access url to get info are: \n" + instance.public_dns_name
        send_email(instance_subject,instance_message)
        return instance.public_dns_name


#Saving Data in DynamoDB
def dynamodb_insert_data(date,distance,percentage,level):
  dynamodb = boto3.resource('dynamodb')
  table = dynamodb.Table('Sensor_Data')
  table.put_item(
        Item={
            'date': date,
            'distance': distance,
            'percentage': percentage,
            'level': level,
        }
    )



#Main program 
if __name__ == '__main__':
    
    level = -1
    whole = 16.5
    ec2_start_instance()
    url = ec2_get_dns_name()
    print("The access url to get info are: " + url)
    print('Stop by pressing CTRL + C')
    try:
        while True:       
            dist,date= distance()
            part = whole - dist
            perc = percentage(part,whole)

            time.sleep(1)
            if(perc >= 80):
                if(level != 4):
                    level = 4
                    print("Date: %s - Distance: %s cm - Percentage: %s %% - Level: %s" % (date,dist,perc,level))
                    try:
                        dynamodb_insert_data(date,str(dist),str(perc),str(level))
                        blynk_send_data(date,dist,perc,level)
                        alert_subject = 'ALERT: Water Level Monitoring System'
                        alert_message = 'Alert received from your Water Level Monitoring System. The filling has reached a critical point. Check the system before eventual damage.'
                        send_email(alert_subject,alert_message)
                    except Exception as e: print(e)
            elif(perc < 60 and perc >= 45):   
                if(level != 3):
                    level = 3
                    print("Date: %s - Distance: %s cm - Percentage: %s %% - Level: %s" % (date,dist,perc,level))
                    dynamodb_insert_data(date,str(dist),str(perc),str(level))
                    blynk_send_data(date,dist,perc,level)
            elif(perc < 45 and perc >= 30):
                if(level != 2):
                    level = 2
                    print("Date: %s - Distance: %s cm - Percentage: %s %% - Level: %s" % (date,dist,perc,level))
                    dynamodb_insert_data(date,str(dist),str(perc),str(level))
                    blynk_send_data(date,dist,perc,level)
            elif(perc < 30 and perc >= 15):
                if(level != 1):
                    level = 1
                    print("Date: %s - Distance: %s cm - Percentage: %s %% - Level: %s" % (date,dist,perc,level))
                    dynamodb_insert_data(date,str(dist),str(perc),str(level))
                    blynk_send_data(date,dist,perc,level)
            elif(perc < 15 and perc >=0):
                if(level != 0):
                    level = 0
                    print("Date: %s - Distance: %s cm - Percentage: %s %% - Level: %s" % (date,dist,perc,level))
                    dynamodb_insert_data(date,str(dist),str(perc),str(level))
                    blynk_send_data(date,dist,perc,level)
            else:
                level = -1         

    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
    except:
        print('An error occured during measurement')
    finally:
        ec2_stop_instance()
        GPIO.cleanup()
        