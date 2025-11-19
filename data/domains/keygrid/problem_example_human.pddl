(define (problem simple-grid-problem)
  (:domain keygrid)

  (:objects
    place1 place2 - place
    key1 - key
    square - shape
  )

  (:init

    ;; connectivity
    (conn place1 place2)

    ;; shapes
    (shape square)
    (key-shape key1 square)
    (lock-shape place2 square)

    ;; initial states
    (at-robot place1)
    (at key1 place1)
    (locked place2)
    (arm-empty)

    ;; by default, place1 is open
    (open place1)
    
  )

  (:goal
    (at-robot place2)
  )
)