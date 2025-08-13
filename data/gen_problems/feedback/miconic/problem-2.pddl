(define (problem miconic-prob-4f-4p)
  (:domain miconic)

  (:objects
    p1 p2 p3 p4 - passenger
    f1 f2 f3 f4 - floor
  )

  (:init
    (origin p1 f2)
    (destin p1 f4)
    (not-boarded p1)
    (not-served p1)
    (origin p2 f2)
    (destin p2 f1)
    (not-boarded p2)
    (not-served p2)
    (origin p3 f3)
    (destin p3 f4)
    (not-boarded p3)
    (not-served p3)
    (origin p4 f1)
    (destin p4 f4)
    (not-boarded p4)
    (not-served p4)
    (above f1 f2)
    (above f1 f3)
    (above f1 f4)
    (above f2 f3)
    (above f2 f4)
    (above f3 f4)
    (lift-at f4)
  )

  (:goal (and
    (served p1)
    (served p2)
    (served p3)
    (served p4)
  ))
)
