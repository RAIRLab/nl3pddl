(define (domain checkers-jumping)
    (:requirements :strips :typing)
    
    (:types
        space
        checker
    )

    (:predicates
        (at ?c - checker ?s - space)
        (empty ?s - space)
        (right-of ?s1 - space ?s2 - space)
        (left-of ?s1 - space ?s2 - space)
        (is-red ?c - checker)
        (is-blue ?c - checker)
    )

    (:action slide-red
        :parameters (?c - checker ?from - space ?to - space)
        :precondition (and 
            (at ?c ?from) 
            (empty ?to) 
            (is-red  ?c) 
            (right-of ?from ?to)
        )
        :effect (and 
            (not (at ?c ?from))
            (at ?c ?to) 
            (not (empty ?to))
            (empty ?from)
        )
    )
    
    (:action slide-blue
        :parameters (?c - checker ?from - space ?to - space)
        :precondition (and 
            (at ?c ?from) 
            (empty ?to) 
            (is-blue ?c) 
            (left-of  ?from ?to)
        )
        :effect (and 
            (not (at ?c ?from))
            (at ?c ?to)
            (not (empty ?to))
            (empty ?from)
        )
    )
    
    (:action jump-red 
        :parameters (?c ?b - checker ?from ?mid ?to - space)
        :precondition (and
            (at ?c ?from)
            (is-red ?c)
            (at ?b ?mid)
            (is-blue  ?b)
            (empty ?to)
            (right-of ?from ?mid)
            (right-of ?mid   ?to)
        )
        :effect (and
            (not (at ?c ?from))
            (at ?c ?to)
            (not (empty ?to))
            (empty ?from)
        )
    )
    
    (:action jump-blue 
        :parameters (?c ?b - checker ?from ?mid ?to - space)
        :precondition (and
            (at ?c ?from)
            (is-blue ?c)
            (at ?b ?mid)
            (is-red  ?b)
            (empty ?to)
            (left-of ?from ?mid)
            (left-of ?mid   ?to)
        )
        :effect (and
            (not (at ?c ?from))
            (at ?c ?to)
            (not (empty ?to))
            (empty ?from)
        )
    )
)