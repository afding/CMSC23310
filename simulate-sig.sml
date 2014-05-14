signature SIMULATE = sig
    val enqueue = Network.network * Message.message -> Network.network;
    (* extract will raise an exception if the network is empty. *)
    val extract = Network.network -> Network.network * Message.message;
    val simulate = int * int * int * Event.event list -> unit;
