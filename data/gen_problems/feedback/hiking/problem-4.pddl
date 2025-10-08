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
    (adjacent loc1 loc3)
    (adjacent loc3 loc1)
    (adjacent loc1 loc5)
    (adjacent loc5 loc1)
    (adjacent loc1 loc6)
    (adjacent loc6 loc1)
    (adjacent loc1 loc8)
    (adjacent loc8 loc1)
    (adjacent loc2 loc3)
    (adjacent loc3 loc2)
    (adjacent loc2 loc4)
    (adjacent loc4 loc2)
    (adjacent loc2 loc5)
    (adjacent loc5 loc2)
    (adjacent loc2 loc6)
    (adjacent loc6 loc2)
    (adjacent loc3 loc5)
    (adjacent loc5 loc3)
    (adjacent loc3 loc6)
    (adjacent loc6 loc3)
    (adjacent loc3 loc7)
    (adjacent loc7 loc3)
    (adjacent loc3 loc8)
    (adjacent loc8 loc3)
    (adjacent loc4 loc7)
    (adjacent loc7 loc4)
    (adjacent loc4 loc9)
    (adjacent loc9 loc4)
    (adjacent loc5 loc8)
    (adjacent loc8 loc5)
    (adjacent loc5 loc9)
    (adjacent loc9 loc5)
    (adjacent loc6 loc9)
    (adjacent loc9 loc6)
    (isHill loc6)
    (isHill loc2)
    (isHill loc7)
    (isHill loc4)
    (isWater loc8)
    (isWater loc5)
    (isWater loc3)
    (isGoal loc9)
  )

  (:goal (at loc9))

)