(define (problem grid-problem-13-6-6-6)
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
    place12 - place
    place13 - place
    key1 - key
    key2 - key
    key3 - key
    key4 - key
    key5 - key
    key6 - key
    shape1 - shape
    shape2 - shape
    shape3 - shape
    shape4 - shape
    shape5 - shape
    shape6 - shape
  )
  (:init
    (conn place1 place2)
    (conn place2 place1)
    (conn place1 place3)
    (conn place3 place1)
    (conn place1 place4)
    (conn place4 place1)
    (conn place1 place5)
    (conn place5 place1)
    (conn place1 place8)
    (conn place8 place1)
    (conn place1 place10)
    (conn place10 place1)
    (conn place1 place11)
    (conn place11 place1)
    (conn place1 place13)
    (conn place13 place1)
    (conn place2 place4)
    (conn place4 place2)
    (conn place2 place9)
    (conn place9 place2)
    (conn place2 place11)
    (conn place11 place2)
    (conn place2 place13)
    (conn place13 place2)
    (conn place3 place4)
    (conn place4 place3)
    (conn place3 place5)
    (conn place5 place3)
    (conn place3 place7)
    (conn place7 place3)
    (conn place3 place8)
    (conn place8 place3)
    (conn place3 place11)
    (conn place11 place3)
    (conn place3 place13)
    (conn place13 place3)
    (conn place4 place5)
    (conn place5 place4)
    (conn place4 place6)
    (conn place6 place4)
    (conn place4 place7)
    (conn place7 place4)
    (conn place4 place8)
    (conn place8 place4)
    (conn place4 place9)
    (conn place9 place4)
    (conn place4 place11)
    (conn place11 place4)
    (conn place5 place6)
    (conn place6 place5)
    (conn place5 place7)
    (conn place7 place5)
    (conn place5 place9)
    (conn place9 place5)
    (conn place5 place12)
    (conn place12 place5)
    (conn place6 place9)
    (conn place9 place6)
    (conn place6 place11)
    (conn place11 place6)
    (conn place6 place13)
    (conn place13 place6)
    (conn place7 place11)
    (conn place11 place7)
    (conn place7 place12)
    (conn place12 place7)
    (conn place8 place9)
    (conn place9 place8)
    (conn place8 place10)
    (conn place10 place8)
    (conn place8 place11)
    (conn place11 place8)
    (conn place8 place12)
    (conn place12 place8)
    (conn place9 place10)
    (conn place10 place9)
    (conn place10 place11)
    (conn place11 place10)
    (conn place11 place12)
    (conn place12 place11)
    (conn place11 place13)
    (conn place13 place11)
    (key-shape key1 shape6)
    (key-shape key2 shape4)
    (key-shape key3 shape2)
    (key-shape key4 shape5)
    (key-shape key5 shape6)
    (key-shape key6 shape1)
    (lock-shape place9 shape3)
    (locked place9)
    (lock-shape place12 shape2)
    (locked place12)
    (lock-shape place7 shape1)
    (locked place7)
    (lock-shape place5 shape2)
    (locked place5)
    (lock-shape place8 shape1)
    (locked place8)
    (lock-shape place13 shape6)
    (locked place13)
    (at key1 place11)
    (at key2 place10)
    (at key3 place13)
    (at key4 place8)
    (at key5 place1)
    (at key6 place6)
    (at-robot place1)
    (open place1)
    (arm-empty)
  )
  (:goal
    (at-robot place12)
  )
)
