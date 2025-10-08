;; Hiking problem generator
;; Locations: 11, Hills: 5, Waters: 5, Seed: None

(define (problem hiking-problem-11-5-5)
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
    loc10 - loc
    loc11 - loc
  )

  (:init
    (at loc1)
    (adjacent loc1 loc2)
    (adjacent loc2 loc1)
    (adjacent loc1 loc4)
    (adjacent loc4 loc1)
    (adjacent loc1 loc8)
    (adjacent loc8 loc1)
    (adjacent loc1 loc9)
    (adjacent loc9 loc1)
    (adjacent loc1 loc10)
    (adjacent loc10 loc1)
    (adjacent loc2 loc4)
    (adjacent loc4 loc2)
    (adjacent loc2 loc6)
    (adjacent loc6 loc2)
    (adjacent loc2 loc8)
    (adjacent loc8 loc2)
    (adjacent loc3 loc4)
    (adjacent loc4 loc3)
    (adjacent loc3 loc5)
    (adjacent loc5 loc3)
    (adjacent loc3 loc6)
    (adjacent loc6 loc3)
    (adjacent loc4 loc5)
    (adjacent loc5 loc4)
    (adjacent loc4 loc6)
    (adjacent loc6 loc4)
    (adjacent loc4 loc8)
    (adjacent loc8 loc4)
    (adjacent loc4 loc11)
    (adjacent loc11 loc4)
    (adjacent loc5 loc6)
    (adjacent loc6 loc5)
    (adjacent loc5 loc7)
    (adjacent loc7 loc5)
    (adjacent loc5 loc8)
    (adjacent loc8 loc5)
    (adjacent loc5 loc10)
    (adjacent loc10 loc5)
    (adjacent loc5 loc11)
    (adjacent loc11 loc5)
    (adjacent loc6 loc7)
    (adjacent loc7 loc6)
    (adjacent loc6 loc8)
    (adjacent loc8 loc6)
    (adjacent loc6 loc9)
    (adjacent loc9 loc6)
    (adjacent loc6 loc10)
    (adjacent loc10 loc6)
    (adjacent loc6 loc11)
    (adjacent loc11 loc6)
    (adjacent loc7 loc10)
    (adjacent loc10 loc7)
    (adjacent loc8 loc9)
    (adjacent loc9 loc8)
    (adjacent loc9 loc10)
    (adjacent loc10 loc9)
    (adjacent loc9 loc11)
    (adjacent loc11 loc9)
    (adjacent loc10 loc11)
    (adjacent loc11 loc10)
    (isHill loc5)
    (isHill loc6)
    (isHill loc7)
    (isHill loc2)
    (isHill loc10)
    (isWater loc9)
    (isWater loc3)
    (isWater loc4)
    (isWater loc8)
    (isGoal loc11)
  )

  (:goal (at loc11))

)