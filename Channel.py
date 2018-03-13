from collections import deque

#class for channel
class Channel:

    #initialize channel
    def __init__(self, name, maxlength):
        self.name = name
        #messages 
        self.posts = deque([], maxlen=maxlength) 

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

    #Test post append/removal
    a = Channel('Channel2',2)
    a.post('a')
    a.post('b')
    a.post('c')
    assert a.posts.count('a') == 0
    assert a.posts.count('b') == 1
    assert a.posts.count('c') == 1
