 (let Ackermann = (fun (0::n) -> (n + 1) | (m::0) -> (Ackermann ((m - 1)::1)) | (m::n) -> (Ackermann ((m - 1)::(Ackermann (m::(n - 
1))))) nuf) in Ackermann (1::0) tel)
