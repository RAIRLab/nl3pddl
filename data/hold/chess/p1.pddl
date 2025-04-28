(define (problem problem_name)
  (:domain KnightTour)
  
  (:objects
    n1 n2 n3 n4 - pos
  )

  (:init
    ;; Knight begins at (n1, n4)
    (at n1 n4)
    (visited n1 n4)

    ;; Everything else starts unvisited:
    (unvisited n1 n1)
    (unvisited n1 n2)
    (unvisited n1 n3)

    (unvisited n2 n1)
    (unvisited n2 n2)
    (unvisited n2 n3)
    (unvisited n2 n4)

    (unvisited n3 n1)
    (unvisited n3 n2)
    (unvisited n3 n3)
    (unvisited n3 n4)

    (unvisited n4 n1)
    (unvisited n4 n2)
    (unvisited n4 n3)

    ;; increase_one relationships
    (increase_one n1 n2)
    (increase_one n2 n1)
    (increase_one n2 n3)
    (increase_one n3 n2)
    (increase_one n3 n4)
    (increase_one n4 n3)

    ;; increase_two relationships
    (increase_two n1 n3)
    (increase_two n3 n1)
    (increase_two n2 n4)
    (increase_two n4 n2)
  )

  ;; Goal: visit these squares
  (:goal (and
     (visited n1 n1)
     (visited n1 n2)
     (visited n1 n3)
     (visited n1 n4)
  ))
)
