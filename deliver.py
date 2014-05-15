import message
import computer

# Checks if there is a majority of strings of a certain type.
def is_majority(mlist, n, typ, pid):
    return len(filter((lambda x: x.typ == typ and x.pid == pid), mlist)) > n/2

# Gets all messages in a list with given typ and pid.
def get_relevant(mlist, n, typ, pid):
    return filter((lambda x: x.typ == typ and x.pid == pid), mlist)

# Determines the new proposal value among a list of (relevant) PROMISE msgs.
# v is the default value (i.e. client's value).
def new_prop_value(mlist, v):
    max_old_pid = -1
    assoc_old_value = -1
    for m in mlist:
        # Takes advantage of None > n is False for any n.
        if m.old_pid > max_old_pid:
            max_old_pid = m.old_pid
            assoc_old_value = m.old_val
    if max_old_pid == -1:
        assoc_old_value = v
    return assoc_old_value

# Takes a proposer and a message, network N, and acceptors A.
def deliver_proposer(c, m, N, A):
    if c.state == "P_init":
        if m.typ != "PROPOSE":
            return
        else:
            c.pid = N.get_pid()
            c.value = m.val
        for a in A:
            to_send = message.Message("PREPARE", c.label, a.label, c.pid,
                                      None, None, None)
            N.enqueue(to_send)
        c.state = "P_wait_promise"
        return

    # Assuming 1 proposal at a time, hence, all PROMISE messages are about this
    # proposal.
    elif c.state == "P_wait_promise":
        c.mlist.append(m)
        if not is_majority(c.mlist, len(A), "PROMISE", c.pid):
            return
        else:
            a = get_relevant(c.mlist, len(A), "PROMISE", c.pid)
            # Remove these from c.mlist:
            c.mlist = [x for x in list(c.mlist) if x not in a]
            new_val = new_prop_value(a, c.value)
            for a in A:
                to_send = message.Message("ACCEPT", c.label, a.label, c.pid,
                                          new_val, None, None)
                N.enqueue(to_send)
            c.state = "P_wait_accepted"
            return

    # Now to wait for a majority of ACCEPTED or REJECTED messages.
    elif c.state == "P_wait_accepted":
        c.mlist.append(m)
        if not is_majority(c.mlist, len(A), "REJECTED", c.pid):
            if not is_majority(c.mlist, len(A), "ACCEPTED", c.pid):
                return
            else:
                # Assuming m is part of the majority, since a
                # majority only happened once m was in the list.
                c.consensus = "P%r has reached consensus (proposed %r, accepted %r)" % (c.label, c.value, m.val)
                c.state = "P_final"
                return
        else:
            # Try again with new pid.
            c.pid = N.get_pid()
            for a in A:
                to_send = message.Message("PREPARE", c.label, a.label, c.pid,
                                          None, None, None)
                N.enqueue(to_send)
            c.state = "P_wait_promise"
            return
    else: # c.state = "P_final":
        return



# Takes an acceptor and a message, network N, and acceptors A.
def deliver_acceptor(c, m, N, P):
    p = m.src # so p is a label already.
    if m.typ == "PREPARE" and m.pid < c.pid:
        # Silently drop prepares with low pid.
        return
    elif m.typ == "PREPARE" and m.pid > c.pid:
        # Send promise and updates its pid (for Acceptor, pid = highest promise)
        c.pid = m.pid
        to_send = message.Message("PROMISE", c.label, p, c.pid,
                                  None, c.old_pid, c.old_val)
        N.enqueue(to_send)
        return
    elif m.typ == "ACCEPT" and m.pid < c.pid:
        # As per agreement with PROMISE, we must reply with REJECTED.
        to_send = message.Message("REJECTED", c.label, p, m.pid,
                                  None, None, None)
        N.enqueue(to_send)
    elif m.typ == "ACCEPT" and m.pid == c.pid:
        # We accept this value, and modify old_pid and old_val as well, since
        # this will be the future "newest accepted proposal".
        c.old_pid = m.pid
        c.old_val = m.val
        to_send = message.Message("ACCEPTED", c.label, p, m.pid,
                                  m.val, None, None)
        N.enqueue(to_send)
    else:
        s = "deliver_acceptor: unexpected m.typ: %s" % m.typ
        raise ValueError(s)

def deliver(c, m, N, P, A):
    if c.role == "Proposer":
        deliver_proposer(c, m, N, A)
    else:
        deliver_acceptor(c, m, N, P)
