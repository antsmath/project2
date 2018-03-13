import hashlib, binascii

class Flacker:

    #initialize Flacker
    def __init__(self, login_name, password):
        self.login_name = login_name

        #hash password
        byte_login_name = bytes(login_name, 'utf8')
        byte_password = bytes(password, 'utf8')
        hash_password = hashlib.pbkdf2_hmac('sha256', byte_password, byte_login_name, 100000)
        self.password = binascii.hexlify(hash_password)

    #Check password Flacker
    def password_equals(self, password):

        #hash password and check
        byte_login_name = bytes(self.login_name, 'utf8')
        byte_password = bytes(password, 'utf8')
        hash_password = hashlib.pbkdf2_hmac('sha256', byte_password, byte_login_name, 100000)
        return self.password == binascii.hexlify(hash_password) 

#Test 
if __name__ == "__main__":
    #Test initialize
    a = Flacker("Amy","Password")
    assert a.login_name == "Amy"
    assert a.password is not None

    #Test password checker
    b = Flacker("Joe","Password")
    assert b.password_equals("Password")
    assert not b.password_equals("password")