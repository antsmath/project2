import hashlib, binascii

#class for users of Flack
class Flacker:

    #initialize Flacker
    def __init__(self, user_name, password):
        self.user_name = user_name

        #hash password
        byte_user_name = bytes(str(user_name), 'utf8')
        byte_password = bytes(str(password), 'utf8')
        hash_password = hashlib.pbkdf2_hmac('sha256', byte_password, byte_user_name, 100000)
        self.password = binascii.hexlify(hash_password)

    #Hash Flacker
    def __hash__(self):
        return hash((self.user_name, self.password))

    #equals Flacker
    def __eq__(self, other):
        if not isinstance(other, type(self)): 
            return NotImplemented

        return self.user_name == other.user_name and self.password == other.password

    #Check password Flacker
    def password_equals(self, password):
        #hash password and check
        byte_user_name = bytes(self.user_name, 'utf8')
        byte_password = bytes(password, 'utf8')
        hash_password = hashlib.pbkdf2_hmac('sha256', byte_password, byte_user_name, 100000)
        return self.password == binascii.hexlify(hash_password) 

#Test 
if __name__ == '__main__':
    #Test initialize
    a = Flacker('Amy','Password')
    assert a.user_name == 'Amy'
    assert a.password is not None

    #Test hash
    b1 = Flacker('Amy','1')
    b2 = Flacker('Amy','1')
    b3 = Flacker('Bob','1')
    assert b1.__hash__() == b2.__hash__()
    assert not b1.__hash__() == b3.__hash__()

    #Test eq
    c1 = Flacker('Amy','1')
    c2 = Flacker('Amy','1')
    c3 = Flacker('Bob','1')
    c4 = 'Amy'
    assert c1.__eq__(c2)
    assert not c1.__eq__(c3)
    assert c1.__eq__(c4) is NotImplemented 

    #Test password checker
    d = Flacker('Joe','Password')
    d = Flacker('Joe1','Password')
    assert d.password_equals('Password')
    assert not d.password_equals('password')

    #Test password hash is different with different name
    d1 = Flacker('Joe1','Password')
    d2 = Flacker('Joe1','Password')
    d3 = Flacker('Joe2','Password')
    assert d1.password == d2.password
    assert not d1.password == d3.password