import message
import computer

class Network:
# The network will also keep track of the proposal numbers.

    def __init__(self):
        self.mlist = []
        self.next_ticket = 0

    def __repr__(self):
        return "Network(mlist=%r,next_ticket=%r)" % ("\n".join(repr(m) for m in self.mlist), self.next_ticket)

    def enqueue(self, m):
        self.mlist.append(m)

    def get_pid(self):
        self.next_ticket += 1
        return self.next_ticket

# P and A will be set of proposers and acceptors.
    def extract(self, P, A):
        m = next((m
                 for m
                 in self.mlist
                 if not(computer.search(m.src, P, A).failed or
                        computer.search(m.dst, P, A).failed)), None)
        if m is not None:
            self.mlist.remove(m)
        return m
