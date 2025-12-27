class Queue:
    def __init__(self, n):
        self.queue = []
        self.pos =0
    def Push(self, a):
        self.queue.append(a)
    def Pop(self):
        a= self.queue[self.pos]
        self.pos+=1
        return a


if __name__ =='__main__':
    s = input()
    q = Queue(len(s))
    for i in s:
        q.Push(i)
    left = 0
    right =0
    while True:
        a = q.Pop()
        if a =='(':
            left+=1
            continue
        elif a ==')':
            left-=1
            continue
        if a =='B':
            print(left)
            break