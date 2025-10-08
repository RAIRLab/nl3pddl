(define (problem grid-problem-11-5-5-5)
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
    place10 - place
    place11 - place
    key1 - key
    key2 - key
    key3 - key
    key4 - key
    key5 - key
    shape1 - shape
    shape2 - shape
    shape3 - shape
    shape4 - shape
    shape5 - shape
  )
  (:init
    (conn place1 place2)
    (conn place2 place1)
    (conn place1 place6)
    (conn place6 place1)
    (conn place1 place7)
    (conn place7 place1)
    (conn place1 place9)
    (conn place9 place1)
    (conn place1 place11)
    (conn place11 place1)
    (conn place2 place3)
    (conn place3 place2)
    (conn place2 place4)
    (conn place4 place2)
    (conn place2 place7)
    (conn place7 place2)
    (conn place2 place10)
    (conn place10 place2)
    (conn place3 place4)
    (conn place4 place3)
    (conn place3 place5)
    (conn place5 place3)
    (conn place3 place6)
    (conn place6 place3)
    (conn place3 place7)
    (conn place7 place3)
    (conn place3 place9)
    (conn place9 place3)
    (conn place3 place10)
    (conn place10 place3)
    (conn place3 place11)
    (conn place11 place3)
    (conn place4 place10)
    (conn place10 place4)
    (conn place4 place11)
    (conn place11 place4)
    (conn place5 place8)
    (conn place8 place5)
    (conn place6 place8)
    (conn place8 place6)
    (conn place6 place10)
    (conn place10 place6)
    (conn place7 place9)
    (conn place9 place7)
    (conn place7 place10)
    (conn place10 place7)
    (conn place7 place11)
    (conn place11 place7)
    (key-shape key1 shape5)
    (key-shape key2 shape2)
    (key-shape key3 shape1)
    (key-shape key4 shape3)
    (key-shape key5 shape4)
    (lock-shape place2 shape2)
    (locked place2)
    (lock-shape place11 shape1)
    (locked place11)
    (lock-shape place6 shape5)
    (locked place6)
    (lock-shape place8 shape1)
    (locked place8)
    (lock-shape place3 shape5)
    (locked place3)
    (at key1 place1)
    (at key2 place4)
    (at key3 place2)
    (at key4 place1)
    (at key5 place9)
    (at-robot place1)
    (open place1)
    (arm-empty)
  )
  (:goal
    (at-robot place6)
  )
)
