(define (problem p1) (:domain bookseller)
(:objects 
    b1 b2 b3 b4 b5 b6 b7 - book
    l1 l2 l3 l4 l5 l6 l7 l8 l9 - location
    d1 d2 - drone
)

(:init
    (book-at b1 l1)
    (book-at b2 l1)
    (book-at b3 l1)
    (book-at b4 l4)
    (book-at b5 l5)
    (book-at b6 l7)
    (book-at b7 l7)
    (drone-at d1 l1)
    (drone-at d2 l7)
    (path l1 l2)
    (path l2 l3)
    (path l3 l4)
    (path l4 l5)
    (path l5 l6)
    (path l6 l7)
    (path l7 l8)
    (path l8 l9)
    (path l9 l1)
    (empty d1)
    (empty d2)
)

(:goal (and
    (book-at b1 l1)
    (book-at b2 l2)
    (book-at b3 l3)
    (book-at b4 l4)
    (book-at b5 l5)
    (book-at b6 l6)
    (book-at b7 l7)
))
)
