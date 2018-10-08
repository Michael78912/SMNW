"""
bugreport.py
this module takes any exception, the app name,
and any other info, and reports it to my email.
"""

import io
import os
import smtplib
from cryptography.fernet import Fernet
import sys
import threading
import traceback
import platform

FYUKYFVKFYVHUFL = b'gAAAAABavaf20Qc-jiOnPXzOsBfr-yhJiVbuBEiyK4cJA3r82f0wXAp5gdgPQ43UxZB7H9O9RgiTCHDb0ngh9CNCRPi03nQssg=='
HIUEFWILEIURFHE = b'_qJoI0kXZlQuHI0-U8BSSKuKQ_Zpp3vQMZGrPKMk8lI='
TMP = os.path.join(
    '/tmp/', 'stderr.tmp') if os.name == 'posix' else os.path.join(os.getenv('TMP'), 'stderr.tmp')


def main(project_name, exception, *other_info):
    """
    main function for sending mail.
    """
    exception.args = [str(arg) for arg in exception.args]
    print(exception.args)
    exception_traceback_details, exception_message = get_details(exception)
    email = build_message(project_name, exception_message,
                          exception_traceback_details, *other_info)
    send_message(email)


def send_message(message):
    """
    sends message to the bug report address
    """
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    # i dont want random people just emailing me!!
    decrypter = Fernet(HIUEFWILEIURFHE)
    data = decrypter.decrypt(FYUKYFVKFYVHUFL).decode()
    server.ehlo()
    server.login('bugreporter.smr@gmail.com', data)
    server.sendmail('bugreporter.smr@gmail.com',
                    'bugreporter.smr@gmail.com', message)
    server.close()


def build_message(project, tbmessage, details, *args):
    """
    build and return a email that contains the 
    traceback.
    """

    bottomline = ',\n'.join(args) if len(args) > 0 else 'Nope'
    sender = reciever = 'bugreporter.smr@gmail.com'
    name = os.name
    build = platform.platform()
    email_string = f"""
    From: {sender}
    To: {reciever}
    Subject: bug in {project} on a {name} system :(

    
    platform:
        {build}

    
    details (traceback):
        {details}

    the message (even though it showed up before):
        {tbmessage}

    any extra things?
    
    {bottomline}


    sincerely, automatic message that has no heart :)
    """

    return email_string


def get_details(exception):
    """
    return the details of the traceback
    """

    tbstring = ''.join(traceback.format_exception(
        type(exception), exception, exception.__traceback__))
    tbargs = ', '.join(exception.args)
    return tbstring, tbargs


def default_smr(exception, *args):
    main('stickman\'s new world', exception, *args)


try:
    raise SyntaxError

except BaseException as e:
    main('test', e)
