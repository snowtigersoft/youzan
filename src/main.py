#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2016 - kylinlingh@foxmail.com

import xml.etree.ElementTree as etree
from threading import Thread
import re
import time
import os
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src import apiclient

# get the absolute path
base_dir = os.path.dirname(__file__)
log_file = os.path.join(base_dir, os.path.pardir, 'log.txt')
config_file = os.path.join(base_dir, os.path.pardir, 'config.xml')
record_file = os.path.join(base_dir, os.path.pardir, 'record.txt')
attach_dir = os.path.join(base_dir, os.path.pardir, 'attachment')


def run():
    global cache_total_result
    logging.basicConfig(filename=log_file, level=logging.INFO)
    logging.getLogger("requests").setLevel(logging.WARNING)

    load_config_file()
    cache_total_result = extract_total_result()

    # get_things_done()

    while True:
        now = str(time.ctime())
        print('\nchecking at: ', now)
        logging.info('checking at:{}\n'.format(now))
        get_things_done()
        time.sleep(int(interval))


def extract_total_result():
    result = get_content_from()
    total_number = re.findall('"total_results":"(.*?)"',
                              result, re.S)[0]
    return total_number


def load_config_file():
    global config_file
    global username
    global password
    global email_head
    global email_subject
    global email_content_text
    global app_id
    global app_secret
    global interval
    global mail_server_name
    global leave_message

    tree = etree.parse(config_file)

    username = tree.find('email_config').attrib['username']
    password = tree.find('email_config').attrib['password']
    email_head = tree.find('email_config/from').text
    email_subject = tree.find('email_config/subject').text
    email_content_text = tree.find('email_config/text').text
    app_id = tree.find('youzan_account/app_id').text
    app_secret = tree.find('youzan_account/app_secret').text
    interval = tree.find('interval').text
    mail_server_name = tree.find('email_config/server').text
    leave_message = tree.find('youzan_account/leave_message').text


def get_content_from():
    method = 'kdt.trades.sold.get'  # the method to get the status of orders from youzan's api
    params_dict = {
        'fields': 'tid,orders',  # only get these two kinds of contents from method get(url)
        'page_size': 100,
        'page_no': 1,
        'status': 'WAIT_BUYER_CONFIRM_GOODS'  # sucessful trade
    }
    global app_id
    global app_secret
    api_client = apiclient.ApiClient(app_id, app_secret)
    result = api_client.get(method, **params_dict) \
        .encode('utf-8').decode('unicode-escape')  # transcode from unicode to chinese
    return result


def get_things_done():
    result = get_content_from()

    global leave_message
    pattern = '{"title":"%s","content":"(.*?)"}' % leave_message
    email_addresses = re.findall(pattern, result, re.S)  # get the email addresses
    tids = re.findall('"tid":"(.*?)"},', result, re.S)  # get the seriel numer of orders
    total_result = re.findall('"total_results":"(.*?)"', result, re.S)[0]

    global record_file
    global cache_total_result
    if int(total_result) > int(cache_total_result):
        num_of_mail_to_send = int(total_result) - int(cache_total_result)
        email_addresses_to_send_mail = fix_email_address(
                email_addresses[:num_of_mail_to_send])
        status = send_mail(email_addresses_to_send_mail)
        cache_total_result = total_result
        write_to_file(total_result, tids,
                      email_addresses_to_send_mail, status)


def fix_email_address(addresses):
    result = []
    for each in addresses:
        if not each.endswith('.com'):
            split = each.split('.')
            right_address = str(split[0]) + '.com'
            result.append(right_address)
        else:
            result.append(each)
    return result


def write_to_file(total_results, tids, email_addresses, status):
    global record_file

    with open(record_file, 'a+', encoding='utf-8') as file:
        file.write('\n===================================================='
                   '==========\n')
        time_record = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        file.write(time_record + ' total_result:{}'.format(total_results))
        file.write('\n******************************************************'
                   '********\n')
        file.write('order_id' + '\t' * 5 + 'email_address' + '\t' * 3 + 'status')
        file.write('\n*******************************************************'
                   '*******\n')
        for tid, email_address in zip(tids, email_addresses):
            temp = str(tid + '\t' + email_address + '\t' + str(status) + '\n')
            file.write(temp)
        file.write('=========================================================='
                   '====\n')


def send_mail(addresses):
    if not addresses:
        logging.error('Email addresses is empty, '
                      'check if you can extract the email addresses correctly')
        raise ValueError('Email addresses is empty, '
                         'check if you can extract the email addresses correctly')
    to_email_addresses = addresses
    email = MIMEMultipart()
    email['Subject'] = email_subject
    email['From'] = email_head
    email_content = MIMEText(email_content_text,
                             'plain', 'utf-8')
    email.attach(email_content)

    global attach_dir
    attach_files = os.walk(attach_dir)  # add every file under directory /attachment as an attachment
    for each in attach_files:
        for filename in each[2]:
            file_path = os.path.join(attach_dir, filename)
            print('sending attachment：', file_path)
            logging.info('sending attachment{}'.format(str(file_path)))
            attachment = MIMEText(open(file_path, 'rb').read(),
                                  'base64', 'utf-8')
            attachment["Content-Type"] = 'application/octet-stream'
            attachment.add_header('Content-Disposition',
                                  'attachment',
                                  filename=('gbk', '', filename))
            email.attach(attachment)
    try:
        mail_server = smtplib.SMTP(mail_server_name, 25)  # connect to the mail server
        # mail_server.set_debuglevel(1)
        mail_server.starttls()
        mail_server.login(username, password)
        mail_server.sendmail(username,
                             to_email_addresses, email.as_string())
        print('sended mail successed')
        logging.info('sended mail successed')
        send_result = 'Successed'
    except Exception as e:
        print('send mail failed')
        logging.info('sended mail failed')
        send_result = ('Failed', str(e))
    finally:
        mail_server.close()
    return send_result


def main():
    thread = Thread(target=run, daemon=True)
    thread.start()
    thread.join()


if __name__ == '__main__':
    main()
