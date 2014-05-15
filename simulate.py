import sys

import message
import event
import network
import computer
import deliver
import read_in

def simulate(np, na, tmax, E):
    P, A = [], []
    N = network.Network()
    # To keep labels as ints while separating Proposers and Separators, I use
    # positive ints for Proposers, negative ints for Acceptors.
    for i in range(1,np+1):
        P.append(computer.Computer(i, "Proposer"))
    for i in range(1,na+1):
        A.append(computer.Computer(-i, "Acceptor"))
    # Stepping through the ticks
    for i in range(tmax+1):
        i2 = str(i).rjust(3)
        #print "TICK TOCK: %r" % str(i)
        if len(N.mlist) == 0 and len(E) == 0:
            return
        # Process the event for this tick (if any).
        e = next((x for x in E if x.t == i), None)
        if e is not None:
            E.remove(e)
            for l in e.F:
                c = computer.search(l, P, A)
                c.failed = True
            for l in e.R:
                c = computer.search(l, P, A)
                c.failed = False
            prop_c = computer.search(e.pic, P, A)
            prop_v = e.piv
            if prop_c is not None and prop_v is not None:
                # Message needs a type, src, dst, pid, val, old_pid, old_val).
                m = message.Message("PROPOSE", None, e.pic, None, e.piv, None, None)
                # PRINTING!!!
                print "%s: %s" % (i2, str(m))
                deliver.deliver(prop_c, m, N, P, A)
            else:
                m = N.extract(P, A)
                if m is not None:
                    # PRINTING!!!
                    print "%s: %s" % (i2, str(m))
                    dst = computer.search(m.dst, P, A)
                    deliver.deliver(dst, m, N, P, A)
                else:
                    # No messages delivered this time-step.
                    print "%s:" % i2
        else:
            m = N.extract(P, A)
            if m is not None:
                # PRINTING!!!
                print "%s: %s" % (i2, str(m))
                dst = computer.search(m.dst, P, A)
                deliver.deliver(dst, m, N, P, A)
            else:
                # No messages delivered this time-step.
                print "%s:" % i2
        #print "NETWORK STATUS: %r" % repr(N)

def main(argv=None):
    if argv is None:
        argv = sys.argv
    fname = argv[1]
    np, na, tmax, E = read_in.read(fname)
    simulate(np, na, tmax, E)

if __name__ == "__main__":
    main()
