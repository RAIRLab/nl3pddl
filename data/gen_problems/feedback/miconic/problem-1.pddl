(define (problem miconic-prob-3f-3p)
  (:domain miconic)

  (:objects
    p1 p2 p3 - passenger
    f1 f2 f3 - floor
  )

  (:init
    (origin p1 f2)
    (destin p1 f1)
    (not-boarded p1)
    (not-served p1)
    (origin p2 f3)
    (destin p2 f2)
    (not-boarded p2)
    (not-served p2)
    (origin p3 f2)
    (destin p3 f3)
    (not-boarded p3)
    (not-served p3)
    (above f1 f2)
    (above f1 f3)
    (above f2 f3)
    (lift-at f2)
  )

  (:goal (and
    (served p1)
    (served p2)
    (served p3)
  ))
)
