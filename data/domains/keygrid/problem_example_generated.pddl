;; Places: 4
;; Keys: 2
;; Shapes: 2
;; Locks: 2
;; Seed: 123
(define (problem grid-problem-4-2-2-2)
  (:domain keygrid)
  (:objects
    place1 - place
    place2 - place
    place3 - place
    place4 - place
    key1 - key
    key2 - key
    shape1 - shape
    shape2 - shape
  )
  (:init
    (conn place1 place2)
    (conn place2 place1)
    (conn place1 place3)
    (conn place3 place1)
    (conn place1 place4)
    (conn place4 place1)
    (conn place2 place3)
    (conn place3 place2)
    (conn place3 place4)
    (conn place4 place3)
    (key-shape key1 shape2)
    (key-shape key2 shape2)
    (lock-shape place2 shape1)
    (locked place2)
    (lock-shape place4 shape2)
    (locked place4)
    (at key1 place3)
    (at key2 place2)
    (at-robot place1)
    (open place1)
    (arm-empty)
  )
  (:goal
    (at-robot place2)
  )
)
