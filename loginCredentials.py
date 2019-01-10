import base64

class oAuth:
    def __init__(self, username, password, key=None):
        self.username = username
        self.password = password
        self.key = key

    @property
    def generate_key(self):
        if not self.key:
            self.key = uuid.uuid4().hex
            return self.key
        else:
            return self.key

    def encrypt_login(self):
        return [self.encode(key = self.generate_key, login_string = s) for s in [self.username, self.password]] + [self.generate_key]

    def decrypt_login(self):
        if self.key:
            return [self.decode(key = self.key, enc = s) for s in [self.username, self.password]]

    def encode(self, key, login_string):
        enc = []
        for i in range(len(login_string)):
            key_c = key[i % len(key)]
            enc_c = chr((ord(login_string[i]) + ord(key_c)) % 256)
            enc.append(enc_c)
        return base64.urlsafe_b64encode("".join(enc).encode()).decode()

    def decode(self, key, enc):
        dec = []
        enc = base64.urlsafe_b64decode(enc).decode()
        for i in range(len(enc)):
            key_c = key[i % len(key)]
            dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
            dec.append(dec_c)
        return "".join(dec)
