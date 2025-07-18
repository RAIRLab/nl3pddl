(define (problem bookseller-prob-5loc-4bk-2dr)
  (:domain bookseller)

  (:objects
    book1 book2 book3 book4 - book
    loc1 loc2 loc3 loc4 loc5 - location
    drone1 drone2 - drone
  )

  (:init
    (book-at book1 loc5)
    (book-at book2 loc5)
    (book-at book3 loc4)
    (book-at book4 loc3)

    (drone-at drone1 loc2)
    (empty drone1)
    (drone-at drone2 loc3)
    (empty drone2)

    (path loc1 loc4)
    (path loc4 loc1)
    (path loc2 loc3)
    (path loc3 loc2)
    (path loc3 loc4)
    (path loc4 loc3)
    (path loc4 loc5)
    (path loc5 loc4)
    (path loc5 loc3)
    (path loc3 loc5)
  )

  (:goal (and
    (book-at book1 loc1)
    (book-at book2 loc4)
    (book-at book3 loc5)
    (book-at book4 loc5)
  ))
)
