import hashlib

class ApiProtocol:
    APP_ID_KEY='app_id'
    METHOD_KEY='method'
    TIMESTAMP_KEY='timestamp'
    FORMAT_KEY='format'
    VERSION_KEY='v'
    SIGN_KEY='sign'
    SIGN_METHOD_KEY='sign_method'

    ALLOWED_DEVIATE_SECONDS=600
    ERR_SYSTEM = -1
    ERR_INVALID_APP_ID = 40001
    ERR_INVALID_APP = 40002
    ERR_INVALID_TIMESTAMP = 40003
    ERR_EMPTY_SIGNATURE = 40004
    ERR_INVALID_SIGNATURE = 40005
    ERR_INVALID_METHOD_NAME = 40006
    ERR_INVALID_METHOD = 40007
    ERR_INVALID_TEAM = 40008
    ERR_PARAMETER = 41000
    ERR_LOGIC = 50000

    def sign(self, app_secret, **paramas):
        content = app_secret
        sorted_key = sorted(paramas)
        for key in sorted_key:
            content += str(key) + str(paramas[key])
        content += app_secret
        # return content
        # print(content)
        return self.hash(content)

    def hash(self, content):
        m = hashlib.md5(content.encode(encoding='utf-8'))
        md5value = m.hexdigest()
        return md5value


if __name__ == '__main__':
    test_dict = {
        'method' : 'kdt.item.get',
        'timestamp' : '2016-01-06 20:06:39',
        'format' : 'json',
        'app_id' : 'test',
        'v' : 1.0,
        'sign_method' : 'md5',
        'num_iid' : 3838293428
        }
    app_sert = 'test'

    test = ApiProtocol()

    test.sign(app_sert, **test_dict)






