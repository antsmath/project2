from collections import deque

#class for channel
class Channel:

    #initialize channel
    def __init__(self, name, maxlength):
        self.name = name
        #messages 
        self.posts = deque([], maxlen=maxlength) 

    #Hash Flacker
    def __hash__(self):
        return hash((self.name))

    #equals Flacker
    def __eq__(self, other):
        if not isinstance(other, type(self)): 
            return NotImplemented

        return self.name == other.name

    #post message to channel
    def post(self, message):
        self.posts.append(message)


#Test 
if __name__ == "__main__":
    #Test initialize
    a = Channel('Channel1',2)
    assert a.name == 'Channel1'
    #Test initialize max length
    a.post('abc')
    a.post('abc')
    a.post('abc')
    assert a.posts.count('abc') == 2

    #Test hash
    b1 = Channel('Channel',1)
    b2 = Channel('Channel',2)
    b3 = Channel('Channelb',1)
    assert b1.__hash__() == b2.__hash__()
    assert not b1.__hash__() == b3.__hash__()

    #Test eq
    c1 = Channel('Channel',1)
    c2 = Channel('Channel',2)
    c3 = Channel('Channelb',1)
    c4 = "Channel"
    assert c1.__eq__(c2)
    assert not c1.__eq__(c3)
    assert c1.__eq__(c4) is NotImplemented 

    #Test post append/removal
    d = Channel('Channel2',2)
    d.post('a')
    d.post('b')
    d.post('c')
    assert d.posts.count('a') == 0
    assert d.posts.count('b') == 1
    assert d.posts.count('c') == 1


