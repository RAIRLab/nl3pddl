
(define (domain bookseller)

    (:requirements :strips :typing)

    (:types book location drone capacity - object)

    (:predicates 
        (book-at ?b - book ?l - location)
        (drone-at ?d - drone ?l - location)
        (path ?l1 - location ?l2 - location)
        (empty ?d - drone)
        (first ?b - book ?d - drone)
        (last ?b - book ?d - drone)
        (ontop ?b1 - book ?b2 - book)
    )

    (:action loadFirst
        :parameters (?d - drone ?b - book ?l - location)
        :precondition (and (drone-at ?d ?l) (book-at ?b ?l) (empty ?d))
        :effect (and (not (empty ?d)) (first ?b ?d) (last ?b ?d) (not (book-at ?b ?l)))
    )

    (:action loadBottom
        :parameters (?d - drone ?b1 ?b2 - book ?l - location)
        :precondition (and (drone-at ?d ?l) (book-at ?b2 ?l) (last ?b1 ?d))
        :effect (and (not (last ?b1 ?d)) (not (book-at ?b ?l)) (ontop ?b1 ?b2) (last ?b2 ?d))
    )

    (:action unloadFinal
        :parameters (?d - drone ?b - book ?l - location)
        :precondition (and (drone-at ?d ?l) (first ?b ?d) (last ?b ?d))
        :effect (and (empty ?d) (book-at ?b ?l) (not (last ?b ?d)) (not (first ?b ?d)))
    )

    (:action unloadBottom
        :parameters (?d - drone ?b1 ?b2 - book ?l - location)
        :precondition (and (drone-at ?d ?l) (ontop ?b1 ?b2) (last ?b2 ?d))
        :effect (and (book-at ?b1 ?l) (not (ontop ?b1 ?b2)) (not (last ?b2 ?d)) (last ?b1 ?d))
    )

    (:action flyDrone
        :parameters (?d - drone ?l1 ?l2 - location)
        :precondition (and (drone-at ?d ?l1) (path ?l1 ?l2))
        :effect (and (drone-at ?d ?l2) (not (drone-at ?d ?l1)))
    )
)