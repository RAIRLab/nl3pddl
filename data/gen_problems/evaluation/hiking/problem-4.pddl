;; Hiking problem generator
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
    (adjacent loc1 loc2)
    (adjacent loc2 loc1)
    (adjacent loc1 loc5)
    (adjacent loc5 loc1)
    (adjacent loc1 loc6)
    (adjacent loc6 loc1)
    (adjacent loc1 loc9)
    (adjacent loc9 loc1)
    (adjacent loc2 loc5)
    (adjacent loc5 loc2)
    (adjacent loc2 loc6)
    (adjacent loc6 loc2)
    (adjacent loc2 loc8)
    (adjacent loc8 loc2)
    (adjacent loc2 loc9)
    (adjacent loc9 loc2)
    (adjacent loc3 loc4)
    (adjacent loc4 loc3)
    (adjacent loc3 loc5)
    (adjacent loc5 loc3)
    (adjacent loc3 loc6)
    (adjacent loc6 loc3)
    (adjacent loc3 loc7)
    (adjacent loc7 loc3)
    (adjacent loc4 loc8)
    (adjacent loc8 loc4)
    (adjacent loc4 loc9)
    (adjacent loc9 loc4)
    (adjacent loc5 loc6)
    (adjacent loc6 loc5)
    (adjacent loc6 loc7)
    (adjacent loc7 loc6)
    (adjacent loc6 loc8)
    (adjacent loc8 loc6)
    (adjacent loc6 loc9)
    (adjacent loc9 loc6)
    (adjacent loc7 loc9)
    (adjacent loc9 loc7)
    (adjacent loc8 loc9)
    (adjacent loc9 loc8)
    (isHill loc5)
    (isHill loc6)
    (isHill loc4)
    (isHill loc7)
    (isWater loc3)
    (isWater loc8)
    (isWater loc2)
    (isGoal loc9)
  )

  (:goal (at loc9))

)