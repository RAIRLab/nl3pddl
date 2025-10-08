(define (problem grid-problem-7-3-3-3)
  (:domain grid)
  (:objects
    place1 - place
    place2 - place
    place3 - place
    place4 - place
    place5 - place
    place6 - place
    place7 - place
    key1 - key
    key2 - key
    key3 - key
    shape1 - shape
    shape2 - shape
    shape3 - shape
  )
  (:init
    (conn place1 place2)
    (conn place2 place1)
    (conn place1 place3)
    (conn place3 place1)
    (conn place1 place4)
    (conn place4 place1)
    (conn place1 place6)
    (conn place6 place1)
    (conn place1 place7)
    (conn place7 place1)
    (conn place2 place6)
    (conn place6 place2)
    (conn place2 place7)
    (conn place7 place2)
    (conn place4 place7)
    (conn place7 place4)
    (conn place5 place7)
    (conn place7 place5)
    (key-shape key1 shape3)
    (key-shape key2 shape1)
    (key-shape key3 shape3)
    (lock-shape place5 shape1)
    (locked place5)
    (lock-shape place4 shape3)
    (locked place4)
    (lock-shape place2 shape2)
    (locked place2)
    (at key1 place1)
    (at key2 place6)
    (at key3 place5)
    (at-robot place1)
    (open place1)
    (arm-empty)
  )
  (:goal
    (at-robot place4)
  )
)
