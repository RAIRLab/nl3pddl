(define (problem grid-problem-3-1-1-1)
  (:domain grid)
  (:objects
    place1 - place
    place2 - place
    place3 - place
    key1 - key
    shape1 - shape
  )
  (:init
    (conn place1 place2)
    (conn place2 place1)
    (conn place1 place3)
    (conn place3 place1)
    (key-shape key1 shape1)
    (lock-shape place2 shape1)
    (locked place2)
    (at key1 place1)
    (at-robot place1)
    (open place1)
    (arm-empty)
  )
  (:goal
    (at-robot place2)
  )
)
