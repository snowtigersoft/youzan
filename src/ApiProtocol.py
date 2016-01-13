import hashlib


class ApiProtocol:

    APP_ID_KEY = 'app_id'
    METHOD_KEY = 'method'
    TIMESTAMP_KEY = 'timestamp'
    FORMAT_KEY = 'format'
    VERSION_KEY = 'v'
    SIGN_KEY = 'sign'
    SIGN_METHOD_KEY = 'sign_method'

    def sign(self, app_secret, **paramas):
        content = app_secret
        sorted_key = sorted(paramas)
        for key in sorted_key:
            content += str(key) + str(paramas[key])
        content += app_secret
        # print(content)
        return self.hash(content)

    def hash(self, content):
        m = hashlib.md5(content.encode(encoding='utf-8'))
        md5value = m.hexdigest()
        return md5value

