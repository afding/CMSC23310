structure Network = struct
(* The network will also keep track of the proposal numbers. *)
type network = Message.message list * int
end
