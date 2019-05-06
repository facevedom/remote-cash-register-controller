import os
import logging
import requests
import helpers.lcd_writer
from subprocess import check_output
from helpers.config_loader import load_config

config = load_config()
logging_file_path = "{}/application.log".format(
    config['SYSTEM']['WORKING_DIRECTORY'])


def log_ip_on_lcd():
    lcd_display.lcd_clear()
    lcd_display.lcd_display_string(check_output(
        ['hostname', '-I']).decode('utf-8'), 1)


def log_ngrok_address_on_lcd():
    r = requests.get('http://localhost:4040/api/tunnels')
    ngrok_tunnels = r.json()
    slack_bot_public_url = ngrok_tunnels['tunnels'][0]['public_url']
    jenkins_public_url = ngrok_tunnels['tunnels'][1]['public_url']

    trimmed_bot_url = slack_bot_public_url.replace(
        'https://', '').replace('.ngrok.io', '')
    trimmed_jenkins_url = jenkins_public_url.replace(
        'https://', '').replace('.ngrok.io', '')
    lcd_display.lcd_display_string(trimmed_bot_url, 2)
    lcd_display.lcd_display_string(trimmed_jenkins_url, 2, pos=8)


lcd_display = helpers.lcd_writer.lcd()
log_ip_on_lcd()
log_ngrok_address_on_lcd()

if not os.path.isfile(logging_file_path):
    os.mknod(logging_file_path)

logging.basicConfig(
    filename=logging_file_path,
    filemode='a',
    format='%(asctime)s - PID %(process)d - %(levelname)s - %(message)s',
    level=logging.DEBUG
)
