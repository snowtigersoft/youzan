#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2016 - kylinlingh@foxmail.com

import xml.etree.ElementTree as etree
from threading import Thread
import re
import time
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src import apiclient

# get the absolute path
base_dir = os.path.dirname(__file__)
config_file = os.path.join(base_dir, os.path.pardir, 'config.xml')
record_file = os.path.join(base_dir, os.path.pardir, 'record.txt')
attach_dir = os.path.join(base_dir, os.path.pardir, 'attachment')


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


def run():
    load_config_file()
    while True:
        get_things_done()
        time.sleep(int(interval))


def get_things_done():
    method = 'kdt.trades.sold.get'  # the method to get the status of orders from youzan's api
    params_dict = {
        'fields': 'tid,orders',  # only get these two kinds of contents from method get(url)
        'page_size': 100,
        'page_no': 1,
        'status': 'WAIT_BUYER_CONFIRM_GOODS'  # sucessful trade
    }
    test_object = apiclient.ApiClient(app_id, app_secret)
    result = test_object.get(method, **params_dict) \
        .encode('utf-8').decode('unicode-escape')  # transcode from unicode to chinese
    # print(result)

    email_addresses = re.findall('{"title":"邮件","content":"(.*?)"}',
                                 result, re.S)
    # email_addresses = re.findall('{"title":"QQ邮箱","content":"(.*?)"}', result, re.S) # get the email addresses

    tids = re.findall('"tid":"(.*?)"},', result, re.S)  # get the seriel numer of orders
    # print(tids)
    total_results = re.findall('"total_results":"(.*?)"', result, re.S)[0]

    global record_file
    file = open(record_file, mode='r+', encoding='utf-8')
    pre_total_result = file.readline().split(':')[-1].rstrip('\r\n')  # get the number from file record.txt
    if int(total_results) > int(pre_total_result):
        num_of_mail_to_send = int(total_results) - int(pre_total_result)
        email_addresses_to_send_mail = fix_email_address(
                email_addresses[:num_of_mail_to_send])
        status = send_mail(email_addresses_to_send_mail)
        write_to_file(total_results, tids,
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
    with open(record_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()[1:]

    with open(record_file, 'w', encoding='utf-8') as file:
        file.seek(0, 0)
        file.write('number_of_trades:' + total_results + '\n')
        for line in lines:  # write the primary data
            file.write(line)

        # write the new data
        file.write('\n===================================================='
                   '==========\n')
        time_record = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        file.write(time_record)
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
    # if not isinstance(addresses, list):
    #     raise ValueError('It must be a list')
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
        print('send mail successed')
        send_result = 'Successed'
    except Exception as e:
        print('send mail failed')
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
