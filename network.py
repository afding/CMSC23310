import message

class Network:
# The network will also keep track of the proposal numbers.

    def __init__(self):
        self.mlist = []
        self.next_ticket = 0

    def enqueue(self, m):
        self.mlist.append(m)

    def get_pid(self):
        self.next_ticket += 1
        return self.next_ticket

# P and A will be set of proposers and acceptors.
    def extract(self, P, A):
        m = next(m for m in self.mlist if not(m.src.fail or m.dst.fail) [None])
        if m is not None:
            self.mlist.remove(m)
        return m
