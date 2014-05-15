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
        # Next variable is to see if a line has been printed
        # for this tick. If not, then print a placeholder line.
        line_printed = False
        if len(N.mlist) == 0 and len(E) == 0:
            break;
        # Process the event for this tick (if any).
        e = next((x for x in E if x.t == i), None)
        if e is not None:
            E.remove(e)
            for l in e.F:
                c = computer.search(l, P, A)
                c.failed = True
                # PRINTING!!!
                line_printed = True
                print "%s: **%s FAILS **" % (i2, message.trans_label(c.label))
            for l in e.R:
                c = computer.search(l, P, A)
                c.failed = False
                # PRINTING!!!
                line_printed = True
                print "%s: **%s RECOVERS **" % (i2, message.trans_label(c.label))
            prop_c = computer.search(e.pic, P, A)
            prop_v = e.piv
            if prop_c is not None and prop_v is not None:
                # Message needs a type, src, dst, pid, val, old_pid, old_val).
                m = message.Message("PROPOSE", None, e.pic, None, e.piv, None, None)
                # PRINTING!!!
                line_printed = True
                print "%s:%s" % (i2, str(m))
                deliver.deliver(prop_c, m, N, P, A)
            else:
                m = N.extract(P, A)
                if m is not None:
                    # PRINTING!!!
                    line_printed = True
                    print "%s:%s" % (i2, str(m))
                    dst = computer.search(m.dst, P, A)
                    deliver.deliver(dst, m, N, P, A)
                else:
                    # No messages delivered this time-step.
                    # Check line_printed to see if we need placeholder.
                    if not line_printed:
                        # PRINTING!!!
                        line_printed = True
                        print "%s:" % i2
        else:
            # Nothing was extracted from list of events E. Goto N.
            m = N.extract(P, A)
            if m is not None:
                # PRINTING!!!
                line_printed = True
                print "%s:%s" % (i2, str(m))
                dst = computer.search(m.dst, P, A)
                deliver.deliver(dst, m, N, P, A)
            else:
                # No messages delivered this time-step.
                # Check line_printed to see if we need placeholder.
                if not line_printed:
                    # PRINTING!!!
                    line_prtined = True
                    print "%s:" % i2
            #print "NETWORK STATUS: %r" % repr(N)
    print ""
    for p in P:
        print p.consensus

def main(argv=None):
    if argv is None:
        argv = sys.argv
    np, na, tmax, E = read_in.read()
    simulate(np, na, tmax, E)

if __name__ == "__main__":
    main()
