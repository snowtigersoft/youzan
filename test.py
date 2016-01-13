
class Test:
    # global name
    def test(self):
        name = 4
        return name

t = Test()
print(t.test())

#




    # write_to_file(file, total_results, tids, email_addresses)



# import xml.etree.ElementTree as etree
#
# tree = etree.parse('config.xml')
#
# username = tree.find('email_config').attrib['username']
# password = tree.find('email_config').attrib['password']
# email_head = tree.find('email_config/from').text
# email_subject = tree.find('email_config/subject').text
# email_content_text = tree.find('email_config/text').text
# app_id = tree.find('youzan_account/app_id').text
# app_sercert = tree.find('youzan_account/app_secert').text
# time_internal = tree.find('time_internal').text

# print(username)
# print(password)
# print(email_head)
# print(email_subject)
# print(email_content_text)
# print(app_id)
# print(app_sercert)
# print(time_internal)

# import time
#
# def delayrun():
#     print('running')
#
# while True:
#     time.sleep(1)
#     delayrun()

#
# with open('record.txt', 'r', encoding='utf-8') as file:
#     lines = file.readlines()[1:]
#
# cc = ('Successed')
# dd = ('Failed', 'gwg')
# with open('record.txt', 'w', encoding='utf-8') as file:
#     file.seek(0, 0)
#     file.write('g'.rstrip('\r\n') + '\n')
#     for line in lines:
#         file.write(line)
#     file.write(str(cc))
#     file.write(str(dd))
#     file.write('sb' +'\t'*5 + 'gw')
#     # file.write('\n')
#     # content = file.read()
#     # file.seek(0, 0)
#     # file.write('sbw'.rstrip('\r\n') + '\n' + content)
