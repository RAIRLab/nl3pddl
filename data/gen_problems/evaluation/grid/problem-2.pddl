(define (problem grid-problem-5-2-2-2)
  (:domain grid)
  (:objects
    place1 - place
    place2 - place
    place3 - place
    place4 - place
    place5 - place
    key1 - key
    key2 - key
    shape1 - shape
    shape2 - shape
  )
  (:init
    (conn place1 place3)
    (conn place3 place1)
    (conn place1 place4)
    (conn place4 place1)
    (conn place1 place5)
    (conn place5 place1)
    (conn place2 place5)
    (conn place5 place2)
    (conn place3 place4)
    (conn place4 place3)
    (key-shape key1 shape2)
    (key-shape key2 shape1)
    (lock-shape place4 shape2)
    (locked place4)
    (lock-shape place3 shape2)
    (locked place3)
    (at key1 place1)
    (at key2 place2)
    (at-robot place1)
    (open place1)
    (arm-empty)
  )
  (:goal
    (at-robot place4)
  )
)
