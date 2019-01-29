import time
import os
import subprocess
from datetime import datetime
import smtplib

dir_path = os.path.dirname(os.path.realpath(__file__))
interval = 600 																		# Set this to the seconds you'd like between process checks
log_file = '{}\\plex_guardian.log'.format(dir_path)									# Defaults to the script directory
launch_plex = 'C:\\YOUR_PMS_DIRECTORY\\Plex Media Server\\Plex Media Server.exe'	# Enter the full path to your plex media server exe

# smtp details, set the below value to false to disable email alerting
email_alerts_enabled = True
host = 'smtp.gmail.com'
port = 587
user = 'your_email_address@gmail.com'
password = 'your_super_secure_password'
to = 'recipient_of_alerts@email.com'


def is_plex_running():
    status = None
    wait_interval = 2
    print('Checking if Plex Server is running..')
    while status is not 'Running':
        processes = subprocess.Popen('tasklist', stdin=subprocess.PIPE, stderr=subprocess.PIPE,
                                     stdout=subprocess.PIPE).communicate()[0]
        if 'Plex Media Server.exe'.encode() not in processes:
            status = 'Not Running'
            print('Plex Server not running, starting...')
            subprocess.Popen(launch_plex, shell=True)
            if email_alerts_enabled is True:
                send_email()
            time.sleep(wait_interval)
            wait_interval = wait_interval * 2
        else:
            print('Plex is running, going back to sleep..')
            status = 'Running'
    return status


def send_email():
    timenow = get_time()
    server = smtplib.SMTP(host, port)
    server.starttls()
    server.login(user, password)
    SUBJECT = 'Plex Guardian Alert: Plex server not running, attempted restart.'
    TEXT = 'Alert at {} I have restarted Plex for you.\n\nRegards,\nPlex Guardian'.format(timenow)
    message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
    server.sendmail(user, to, message)
    server.quit()
    print('{}: Alert triggered.'.format(timenow))
    log = open(log_file, 'a')
    log.write('{}: Alert triggered.\n'.format(timenow))
    log.close()
    return


def get_time():
    timenow = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return timenow


def main():
    global e
    exception_count = 0
    while exit is not True:  # Intentionally left open for continuous loop
        timenow = get_time()
        try:
            status = is_plex_running()
            for i in range(0, interval):
                os.system('cls')
                print("""Plex Guardian                                              Exceptions: %s
                
Status:     %s
Last Check: %s
                
Sleeping for %s seconds
%s\\%s""") % (exception_count, status, timenow, interval, i, interval)
                time.sleep(1)
        except Exception as e:
            timenow = get_time()
            print('{} : Exception is: {}'.format(timenow, e))
            log = open(log_file, 'a')
            log.write('{} : Exception is: {}\n'.format(timenow, e))
            log.close()
            exception_count += 1
            pass


if __name__ == '__main__':
    main()
