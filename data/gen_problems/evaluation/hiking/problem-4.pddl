;; Hiking problem generator (solvable version)
;; Locations: 9, Hills: 4, Waters: 4, Seed: None

(define (problem hiking-problem-9-4-4)
  (:domain hiking)

  (:objects
    loc1 - loc
    loc2 - loc
    loc3 - loc
    loc4 - loc
    loc5 - loc
    loc6 - loc
    loc7 - loc
    loc8 - loc
    loc9 - loc
  )

  (:init
    (at loc1)
    (adjacent loc1 loc5)
    (adjacent loc1 loc6)
    (adjacent loc2 loc3)
    (adjacent loc2 loc4)
    (adjacent loc2 loc5)
    (adjacent loc2 loc8)
    (adjacent loc2 loc9)
    (adjacent loc3 loc2)
    (adjacent loc3 loc4)
    (adjacent loc3 loc7)
    (adjacent loc3 loc8)
    (adjacent loc3 loc9)
    (adjacent loc4 loc2)
    (adjacent loc4 loc3)
    (adjacent loc4 loc5)
    (adjacent loc4 loc6)
    (adjacent loc4 loc8)
    (adjacent loc5 loc1)
    (adjacent loc5 loc2)
    (adjacent loc5 loc4)
    (adjacent loc5 loc8)
    (adjacent loc5 loc9)
    (adjacent loc6 loc1)
    (adjacent loc6 loc4)
    (adjacent loc6 loc9)
    (adjacent loc7 loc3)
    (adjacent loc7 loc8)
    (adjacent loc8 loc2)
    (adjacent loc8 loc3)
    (adjacent loc8 loc4)
    (adjacent loc8 loc5)
    (adjacent loc8 loc7)
    (adjacent loc9 loc2)
    (adjacent loc9 loc3)
    (adjacent loc9 loc5)
    (adjacent loc9 loc6)
    (isHill loc3)
    (isHill loc5)
    (isHill loc6)
    (isHill loc7)
    (isGoal loc9)
  )

  (:goal (at loc9))
)
