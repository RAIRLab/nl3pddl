(define (problem grid-problem-9-4-4-4)
  (:domain grid)
  (:objects
    place1 - place
    place2 - place
    place3 - place
    place4 - place
    place5 - place
    place6 - place
    place7 - place
    place8 - place
    place9 - place
    key1 - key
    key2 - key
    key3 - key
    key4 - key
    shape1 - shape
    shape2 - shape
    shape3 - shape
    shape4 - shape
  )
  (:init
    (conn place1 place2)
    (conn place2 place1)
    (conn place1 place3)
    (conn place3 place1)
    (conn place1 place5)
    (conn place5 place1)
    (conn place1 place6)
    (conn place6 place1)
    (conn place1 place7)
    (conn place7 place1)
    (conn place2 place3)
    (conn place3 place2)
    (conn place2 place4)
    (conn place4 place2)
    (conn place2 place5)
    (conn place5 place2)
    (conn place2 place6)
    (conn place6 place2)
    (conn place2 place8)
    (conn place8 place2)
    (conn place3 place5)
    (conn place5 place3)
    (conn place3 place7)
    (conn place7 place3)
    (conn place4 place5)
    (conn place5 place4)
    (conn place4 place6)
    (conn place6 place4)
    (conn place4 place7)
    (conn place7 place4)
    (conn place4 place8)
    (conn place8 place4)
    (conn place5 place6)
    (conn place6 place5)
    (conn place5 place7)
    (conn place7 place5)
    (conn place5 place8)
    (conn place8 place5)
    (conn place6 place7)
    (conn place7 place6)
    (conn place6 place8)
    (conn place8 place6)
    (conn place6 place9)
    (conn place9 place6)
    (conn place7 place8)
    (conn place8 place7)
    (conn place8 place9)
    (conn place9 place8)
    (key-shape key1 shape2)
    (key-shape key2 shape3)
    (key-shape key3 shape3)
    (key-shape key4 shape4)
    (lock-shape place2 shape4)
    (locked place2)
    (lock-shape place6 shape3)
    (locked place6)
    (lock-shape place8 shape2)
    (locked place8)
    (lock-shape place7 shape1)
    (locked place7)
    (at key1 place4)
    (at key2 place7)
    (at key3 place1)
    (at key4 place6)
    (at-robot place1)
    (open place1)
    (arm-empty)
  )
  (:goal
    (at-robot place6)
  )
)
