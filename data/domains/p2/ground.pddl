
(define (domain lukasiewiczP2)

    ; See https://en.wikipedia.org/wiki/Hilbert_system#%C5%81ukasiewicz's_P2

    (:requirements :strips :typing)

    (:types formula - object)

    (:predicates
        (undef ?f - formula) ; f is an undefined formula
        (def ?f - formula) ; f is a defined formula
        (implies ?f ?l ?r - formula) ; f is an implication formula with left side l and right side r
        (neg ?f ?a - formula) ; f is a negation of the formula a
        (provable ?f - formula) ; f is a provable formula
    )

    (:action def_imp 
        :parameters (?f ?l ?r - formula)
        :precondition (and (undef ?f) (def ?l) (def ?r))
        :effect (and (def ?f) (not (undef ?f)) (implies ?f ?l ?r))
    )

    (:action def_neg
        :parameters (?f ?a - formula)
        :precondition (and (undef ?f) (def ?a))
        :effect (and (def ?f) (not (undef ?f)) (neg ?f ?a))
    )

    (:action a1
        :parameters (?p ?q ?qp ?pqp - formula)
        :precondition (and 
            (def ?p) (def ?q) (def ?qp) (def ?pqp) 
            (implies ?qp ?q ?p) (implies ?pqp ?p ?qp))
        :effect (provable ?pqp)
    )

    (:action a2 
        :parameters (?p ?q ?r ?qr ?pq ?pr ?pqr ?pqpr ?pqrpqpr - formula)
        :precondition (and 
            (def ?p) (def ?q) (def ?r) (def ?qr) (def ?pq) (def ?pr) (def ?pqr) (def ?pqpr) (def ?pqrpqpr)
            (implies ?qr ?q ?r) (implies ?pq ?p ?q) (implies ?pr ?p ?r) (implies ?pqr ?p ?qr) (implies ?pqpr ?pq ?pr) (implies ?pqrpqpr ?pqr ?pqpr))
        :effect (provable ?pqrpqpr)
    )

    (:action a3
        :parameters (?p ?q ?np ?nq ?nqnp ?qp ?nqnpqp - formula)
        :precondition (and 
            (def ?p) (def ?q) (def ?np) (def ?nq) (def ?nqnp) (def ?qp) (def ?nqnpqp)
            (neg ?np ?p) (neg ?nq ?q) (implies ?nqnp ?nq ?np) (implies ?nqnpqp ?nqnp ?qp))
        :effect (provable ?nqnpqp)
    )

    (:action mp 
        :parameters (?p ?q ?pq - formula)
        :precondition (and 
            (def ?p) (def ?q) (def ?pq)
            (implies ?pq ?p ?q) (provable ?p) (provable ?pq))
        :effect (provable ?q)
    )
)