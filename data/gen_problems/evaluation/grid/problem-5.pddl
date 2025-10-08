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
    (conn place1 place4)
    (conn place4 place1)
    (conn place1 place6)
    (conn place6 place1)
    (conn place1 place7)
    (conn place7 place1)
    (conn place1 place8)
    (conn place8 place1)
    (conn place1 place9)
    (conn place9 place1)
    (conn place2 place3)
    (conn place3 place2)
    (conn place2 place4)
    (conn place4 place2)
    (conn place2 place5)
    (conn place5 place2)
    (conn place2 place6)
    (conn place6 place2)
    (conn place2 place7)
    (conn place7 place2)
    (conn place2 place8)
    (conn place8 place2)
    (conn place2 place10)
    (conn place10 place2)
    (conn place2 place11)
    (conn place11 place2)
    (conn place3 place4)
    (conn place4 place3)
    (conn place3 place6)
    (conn place6 place3)
    (conn place3 place7)
    (conn place7 place3)
    (conn place3 place8)
    (conn place8 place3)
    (conn place3 place10)
    (conn place10 place3)
    (conn place3 place11)
    (conn place11 place3)
    (conn place4 place5)
    (conn place5 place4)
    (conn place4 place6)
    (conn place6 place4)
    (conn place4 place8)
    (conn place8 place4)
    (conn place4 place10)
    (conn place10 place4)
    (conn place4 place11)
    (conn place11 place4)
    (conn place5 place7)
    (conn place7 place5)
    (conn place5 place10)
    (conn place10 place5)
    (conn place6 place10)
    (conn place10 place6)
    (conn place6 place11)
    (conn place11 place6)
    (conn place7 place10)
    (conn place10 place7)
    (conn place7 place11)
    (conn place11 place7)
    (conn place8 place10)
    (conn place10 place8)
    (conn place9 place10)
    (conn place10 place9)
    (conn place10 place11)
    (conn place11 place10)
    (key-shape key1 shape5)
    (key-shape key2 shape4)
    (key-shape key3 shape4)
    (key-shape key4 shape3)
    (key-shape key5 shape3)
    (lock-shape place4 shape4)
    (locked place4)
    (lock-shape place6 shape1)
    (locked place6)
    (lock-shape place2 shape3)
    (locked place2)
    (lock-shape place9 shape3)
    (locked place9)
    (lock-shape place10 shape4)
    (locked place10)
    (at key1 place4)
    (at key2 place6)
    (at key3 place6)
    (at key4 place1)
    (at key5 place4)
    (at-robot place1)
    (open place1)
    (arm-empty)
  )
  (:goal
    (at-robot place9)
  )
)
