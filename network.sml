structure Network = struct
(* The network will also keep track of the proposal numbers. *)
type network = Net of Message.message list * int

fun enqueue(Net(ms, k) : network, m : Message.message) : network =
    Net(m::ms, k)

fun extract(Net(ms, k) : network) : network * message =
    (Net(take(ms, length(ms)-1), k), last(ms))
end
