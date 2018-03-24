from collections import deque
from datetime import datetime

from Flacker import Flacker

#class for channel


class Channel:

    #initialize channel
    def __init__(self, name, maxlength):
        self.name = name
        #messages
        self.messages = deque([], maxlen=maxlength)

    #Hash Flacker
    def __hash__(self):
        return hash((self.name))

    #equals Flacker
    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented

        return self.name == other.name

    #add_message message to channel
    def add_message(self, flacker, message, timestamp=datetime.now()):
        self.messages.append((flacker, message, timestamp))


#Test
if __name__ == "__main__":
    #Test initialize
    f1 = Flacker('flacker_1', 'a')
    a = Channel('Channel_1', 2)
    t1 = datetime.now()
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
    f2 = Flacker('flacker_2', 'a')
    t2 = datetime.now()
    d = Channel('Channel_2', 2)
    d.add_message(f2, 'a', t2)
    d.add_message(f2, 'b', t2)
    d.add_message(f2, 'c', t2)
    assert d.messages.count((f2, 'a', t2)) == 0
    assert d.messages.count((f2, 'b', t2)) == 1
    assert d.messages.count((f2, 'c', t2)) == 1
