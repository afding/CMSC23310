import message

# Searches for a computer given its label.
# Assumes P, A are computers with disjoint sets of labels.
def search(label, P, A):
    return next((x for x in P + A if x.label = label), None)

class Computer:
    
    # We use a state-machine approach. Proposer has several states, Acceptor 1.
    # Also, pid refers to pid of a current proposal for Proposer, and
    # pid of the PROMISE for Acceptor.
    # A Proposer needs a list of messages (because of majority).
    # An Acceptor needs to know its most recently accepted proposal.
    def __init__(self, label, role)
        self.label = label
        self.role = role
        self.failed = False
        if label = "Proposer":
            self.state = "P_init"
            self.pid = -1
            self.value = None
        else: # Acceptor
            self.state = "A"
            self.pid = -1
            self.value = None
        self.mlist = []
        self.old_pid = None
        self.old_val = None
