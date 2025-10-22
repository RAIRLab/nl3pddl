(define (domain lights-out-strips)
    (:requirements :strips :typing)
    (:types
        bubble
    )

    (:predicates
        ;; bubble state
        (on ?b - bubble)
        (off ?b - bubble)

        ;; static neighbor connections
        (connected ?b1 ?b2 - bubble)

        ;; static info: how many neighbors each bubble has
        (one-neighbor ?b - bubble)
        (two-neighbors ?b - bubble)
        (three-neighbors ?b - bubble)
    )

    ;; 1 neighbor
    ;; neighbor is ON
    (:action press-1-1
        :parameters (?b ?n1 - bubble)
        :precondition (and
            (one-neighbor ?b)
            (connected ?b ?n1)
            (on ?n1)
        )
        :effect (and
            (off ?n1)
            (not (on ?n1))
        )
    )

    ;; neighbor is OFF
    (:action press-1-0
        :parameters (?b ?n1 - bubble)
        :precondition (and
            (one-neighbor ?b)
            (connected ?b ?n1)
            (off ?n1)
        )
        :effect (and
            (on ?n1)
            (not (off ?n1))
        )
    )
    
    ;; 2 neighbors
    ;; both ON
    (:action press-2-11
        :parameters (?b ?n1 ?n2 - bubble)
        :precondition (and
            (two-neighbors ?b)
            (connected ?b ?n1)
            (connected ?b ?n2)
            (on ?n1)
            (on ?n2)
        )
        :effect (and
            (off ?n1) (off ?n2)
            (not (on ?n1)) (not (on ?n2))
        )
    )

    ;; both OFF
    (:action press-2-00
        :parameters (?b ?n1 ?n2 - bubble)
        :precondition (and
            (two-neighbors ?b)
            (connected ?b ?n1)
            (connected ?b ?n2)
            (off ?n1)
            (off ?n2)
        )
        :effect (and
            (on ?n1) (on ?n2)
            (not (off ?n1)) (not (off ?n2))
        )
    )

    ;; one ON, one OFF
    (:action press-2-10
        :parameters (?b ?n1 ?n2 - bubble)
        :precondition (and
            (two-neighbors ?b)
            (connected ?b ?n1)
            (connected ?b ?n2)
            (on ?n1)
            (off ?n2)
        )
        :effect (and
            (off ?n1) (on ?n2)
            (not (on ?n1)) (not (off ?n2))
        )
    )

    (:action press-2-01
        :parameters (?b ?n1 ?n2 - bubble)
        :precondition (and
            (two-neighbors ?b)
            (connected ?b ?n1)
            (connected ?b ?n2)
            (off ?n1)
            (on ?n2)
        )
        :effect (and
            (on ?n1) (off ?n2)
            (not (off ?n1)) (not (on ?n2))
        )
    )

    ;; 3 neighbors
    ;; 111
    (:action press-3-111
        :parameters (?b ?n1 ?n2 ?n3 - bubble)
        :precondition (and
            (three-neighbors ?b)
            (connected ?b ?n1) (connected ?b ?n2) (connected ?b ?n3)
            (on ?n1) (on ?n2) (on ?n3)
        )
        :effect (and
            (off ?n1) (off ?n2) (off ?n3)
            (not (on ?n1)) (not (on ?n2)) (not (on ?n3))
        )
    )

    ;; 110
    (:action press-3-110
        :parameters (?b ?n1 ?n2 ?n3 - bubble)
        :precondition (and
            (three-neighbors ?b)
            (connected ?b ?n1) (connected ?b ?n2) (connected ?b ?n3)
            (on ?n1) (on ?n2) (off ?n3)
        )
        :effect (and
            (off ?n1) (off ?n2) (on ?n3)
            (not (on ?n1)) (not (on ?n2)) (not (off ?n3))
        )
    )

    ;; 101
    (:action press-3-101
        :parameters (?b ?n1 ?n2 ?n3 - bubble)
        :precondition (and
            (three-neighbors ?b)
            (connected ?b ?n1) (connected ?b ?n2) (connected ?b ?n3)
            (on ?n1) (off ?n2) (on ?n3)
        )
        :effect (and
            (off ?n1) (on ?n2) (off ?n3)
            (not (on ?n1)) (not (off ?n2)) (not (on ?n3))
        )
    )

    ;; 100
    (:action press-3-100
        :parameters (?b ?n1 ?n2 ?n3 - bubble)
        :precondition (and
            (three-neighbors ?b)
            (connected ?b ?n1) (connected ?b ?n2) (connected ?b ?n3)
            (on ?n1) (off ?n2) (off ?n3)
        )
        :effect (and
            (off ?n1) (on ?n2) (on ?n3)
            (not (on ?n1)) (not (off ?n2)) (not (off ?n3))
        )
    )

    ;; 011
    (:action press-3-011
        :parameters (?b ?n1 ?n2 ?n3 - bubble)
        :precondition (and
            (three-neighbors ?b)
            (connected ?b ?n1) (connected ?b ?n2) (connected ?b ?n3)
            (off ?n1) (on ?n2) (on ?n3)
        )
        :effect (and
            (on ?n1) (off ?n2) (off ?n3)
            (not (off ?n1)) (not (on ?n2)) (not (on ?n3))
        )
    )

    ;; 010
    (:action press-3-010
        :parameters (?b ?n1 ?n2 ?n3 - bubble)
        :precondition (and
            (three-neighbors ?b)
            (connected ?b ?n1) (connected ?b ?n2) (connected ?b ?n3)
            (off ?n1) (on ?n2) (off ?n3)
        )
        :effect (and
            (on ?n1) (off ?n2) (on ?n3)
            (not (off ?n1)) (not (on ?n2)) (not (off ?n3))
        )
    )

    ;; 001
    (:action press-3-001
        :parameters (?b ?n1 ?n2 ?n3 - bubble)
        :precondition (and
            (three-neighbors ?b)
            (connected ?b ?n1) (connected ?b ?n2) (connected ?b ?n3)
            (off ?n1) (off ?n2) (on ?n3)
        )
        :effect (and
            (on ?n1) (on ?n2) (off ?n3)
            (not (off ?n1)) (not (off ?n2)) (not (on ?n3))
        )
    )

    ;; 000
    (:action press-3-000
        :parameters (?b ?n1 ?n2 ?n3 - bubble)
        :precondition (and
            (three-neighbors ?b)
            (connected ?b ?n1) (connected ?b ?n2) (connected ?b ?n3)
            (off ?n1) (off ?n2) (off ?n3)
        )
        :effect (and
            (on ?n1) (on ?n2) (on ?n3)
            (not (off ?n1)) (not (off ?n2)) (not (off ?n3))
        )
    )

)
