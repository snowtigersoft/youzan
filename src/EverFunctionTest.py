import json
import re
import time
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src import ApiClient

def run(internal):
    while True:
        test_myself()
        time.sleep(internal)

def test_myself():
    app_id = '290c00897561005101'
    app_sert = '52813f143dbcc7854815a12043a48213'
    method = 'kdt.trades.sold.get'
    params_dict = {
        # 'fields' : 'orders',
        'page_size' : 100,
        'page_no' : 1,
        'status' : 'WAIT_BUYER_CONFIRM_GOODS' #购买成功，订单状态显示为 卖家已发货
    }
    test_object = ApiClient.ApiClient(app_id, app_sert)

    result = test_object.get(method, **params_dict).encode('utf-8').decode('unicode-escape')
    print(result)

    email_addresses = re.findall('{"title":"邮件","content":"(.*?)"}', result, re.S)
    tids = re.findall('"tid":"(.*?)",', result, re.S)
    # print(tids)
    total_results = re.findall('"total_results":"(.*?)"', result, re.S)[0]

    file = open('record.txt', mode='r+', encoding='utf-8')
    pre_total_result = file.readline().split(':')[-1].rstrip('\r\n')  #得到已经发送过邮件的数量
    #print(pre_total_result)
    if int(total_results) > int(pre_total_result):
        num_of_mail_to_send = int(total_results) - int(pre_total_result)
        email_addresses_to_send_mail = fix_email_address(email_addresses[:num_of_mail_to_send])
        status = send_mail(email_addresses_to_send_mail)
        write_to_file(total_results, tids, email_addresses_to_send_mail, status)


def test_magua():

    app_id = 'e1044d52d066a67990'
    app_sert = '65656b2a6670b7b750bb51c7b31cbff1'
    method = 'kdt.trades.sold.get'
    params_dict = {
        'fields' : 'tid,orders',
        'page_size' : 100,
        'page_no' : 1,
        'status' : 'WAIT_BUYER_CONFIRM_GOODS' #购买成功，订单状态显示为 卖家已发货
    }
    test_object = ApiClient.ApiClient(app_id, app_sert)

    result = test_object.get(method, **params_dict).encode('utf-8').decode('unicode-escape')
    print(result)

    email_addresses = re.findall('{"title":"QQ邮箱","content":"(.*?)"}', result, re.S)
    tids = re.findall('"tid":"(.*?)",', result, re.S)
    total_results = re.findall('"total_results":"(.*?)"', result, re.S)[0]


    file = open('record.txt', mode='r+', encoding='utf-8')
    pre_total_result = file.readline().split(':')[-1]  #得到已经发送过邮件的数量
    #print(pre_total_result)
    if int(total_results) > int(pre_total_result):
        num_of_mail_to_send = int(total_results) - int(pre_total_result)
        email_addresses_to_send_mail = fix_email_address(email_addresses[:num_of_mail_to_send])
        print(email_addresses_to_send_mail)
        email_addresses_to_send_mail = ['kylinlingh@foxmail.com', 'kylinlingh@163.com']
        status = send_mail(email_addresses_to_send_mail)

    # write_to_file(file, total_results, tids, email_addresses)

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

    record_file = 'record.txt'
    with open(record_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()[1:]

    with open(record_file, 'w', encoding='utf-8') as file:
        file.seek(0, 0)
        file.write('number_of_trades:' + total_results + '\n')
        for line in lines:     #写入原来的内容
            file.write(line)
        #增加新的内容
        # file.write( + '\n\n')
        file.write('\n==============================================================\n')
        time_record = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        file.write(time_record )
        file.write('\n**************************************************************\n')
        file.write('order_id' + '\t'*5 + 'email_address' + '\t'*3 + 'status')
        file.write('\n**************************************************************\n')
        for tid, email_address in zip(tids, email_addresses):
            temp = str(tid + '\t' + email_address + '\t' + str(status) + '\n')
            file.write(temp)
        file.write('==============================================================\n')

def send_mail(addresses):

    #邮件账户信息
    from_email_address = 'kylinlingh@foxmail.com'
    password_for_mail = 'lin0607103014'

    if not isinstance(addresses, list):
        raise ValueError('It must be a list')
    to_email_addresses = addresses

    email = MIMEMultipart()

    #邮件头
    email['Subject'] = '测试'
    email['From'] = 'kylinlin'
    email_content = '''
    你好：
        感谢你购买我们的麻瓜教程，祝你学习愉快！
    '''
    email_content = MIMEText(email_content, 'plain', 'utf-8')
    email.attach(email_content)

    base_dir = os.path.dirname(__file__)
    attach_dir = os.path.join(base_dir, os.path.pardir, 'attachment') #获取附件所在的目录
    attach_files = os.walk(attach_dir)
    for each in attach_files:
        for filename in each[2]:
            file_path = os.path.join(attach_dir, filename)
            print('正在发送附件：',file_path)
            attachment = MIMEText(open(file_path, 'rb').read(), 'base64', 'utf-8')
            attachment["Content-Type"] = 'application/octet-stream'
            attachment.add_header('Content-Disposition', 'attachment', filename=('gbk', '', filename))
            email.attach(attachment)
    try:
        qq_server = smtplib.SMTP('smtp.qq.com', 25) #连接qq邮件服务器
        # qq_server.set_debuglevel(1)
        qq_server.starttls()
        qq_server.login(from_email_address, password_for_mail)
        qq_server.sendmail(from_email_address, to_email_addresses, email.as_string())
        print('发送成功')
        send_result = 'Successed'
    except Exception as e:
        print('发送失败')
        send_result = ('Failed', str(e))
    finally:
        qq_server.close()
    return send_result

if __name__ == '__main__':
    # test_myself()
    # test_magua()
    internal_time = 60
    run(internal_time)