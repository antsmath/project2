from collections import deque
from datetime import datetime
from time import strftime


#class for channel


class Channel:

    #initialize channel
    def __init__(self, name, maxlength):
        self.name = name
        #messages
        self.messages = deque([], maxlen=maxlength)

    #Hash channel
    def __hash__(self):
        return hash((self.name))

    #equals channel
    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented

        return self.name == other.name

    #string channel
    def __str__(self):
        return self.name 

    #add_message message to channel
    def add_message(self, user_name, message, timestamp=datetime.now().strftime('%x %X')):
        self.messages.append((user_name, message, timestamp))


#Test
if __name__ == "__main__":
    #Test initialize
    f1 = 'Amy'
    a = Channel('Channel_1', 2)
    t1 = datetime.now().strftime('%x %X')
    assert a.name == 'Channel_1'
    #Test initialize max length
    a.add_message(f1, 'abc', t1)
    a.add_message(f1, 'abc', t1)
    a.add_message(f1, 'abc', t1)
    assert a.messages.count((f1, 'abc', t1)) == 2

    #Test hash
    b1 = Channel('Channel', 1)
    b2 = Channel('Channel', 2)
    b3 = Channel('Channel_b', 1)
    assert b1.__hash__() == b2.__hash__()
    assert not b1.__hash__() == b3.__hash__()

    #Test eq
    c1 = Channel('Channel', 1)
    c2 = Channel('Channel', 2)
    c3 = Channel('Channel_b', 1)
    c4 = "Channel"
    assert c1.__eq__(c2)
    assert not c1.__eq__(c3)
    assert c1.__eq__(c4) is NotImplemented

    #Test add_message append/removal
    f2 = 'Amy'
    t2 = datetime.now().strftime('%x %X')
    d = Channel('Channel_2', 2)
    d.add_message(f2, 'a', t2)
    d.add_message(f2, 'b', t2)
    d.add_message(f2, 'c', t2)
    assert d.messages.count((f2, 'a', t2)) == 0
    assert d.messages.count((f2, 'b', t2)) == 1
    assert d.messages.count((f2, 'c', t2)) == 1

    #Test str
    e = Channel('Channel_1', 2)
    assert str(e) == 'Channel_1'
    assert not str(e) == 'Channel_2'