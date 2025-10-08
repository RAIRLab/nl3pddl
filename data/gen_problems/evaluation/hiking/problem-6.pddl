;; Hiking problem generator
;; Locations: 13, Hills: 6, Waters: 6, Seed: None

(define (problem hiking-problem-13-6-6)
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
    loc12 - loc
    loc13 - loc
  )

  (:init
    (at loc1)
    (adjacent loc1 loc2)
    (adjacent loc2 loc1)
    (adjacent loc1 loc5)
    (adjacent loc5 loc1)
    (adjacent loc1 loc10)
    (adjacent loc10 loc1)
    (adjacent loc1 loc11)
    (adjacent loc11 loc1)
    (adjacent loc1 loc12)
    (adjacent loc12 loc1)
    (adjacent loc2 loc3)
    (adjacent loc3 loc2)
    (adjacent loc2 loc4)
    (adjacent loc4 loc2)
    (adjacent loc2 loc6)
    (adjacent loc6 loc2)
    (adjacent loc2 loc7)
    (adjacent loc7 loc2)
    (adjacent loc2 loc8)
    (adjacent loc8 loc2)
    (adjacent loc2 loc9)
    (adjacent loc9 loc2)
    (adjacent loc2 loc10)
    (adjacent loc10 loc2)
    (adjacent loc2 loc11)
    (adjacent loc11 loc2)
    (adjacent loc2 loc12)
    (adjacent loc12 loc2)
    (adjacent loc3 loc6)
    (adjacent loc6 loc3)
    (adjacent loc3 loc7)
    (adjacent loc7 loc3)
    (adjacent loc3 loc10)
    (adjacent loc10 loc3)
    (adjacent loc4 loc9)
    (adjacent loc9 loc4)
    (adjacent loc5 loc10)
    (adjacent loc10 loc5)
    (adjacent loc5 loc12)
    (adjacent loc12 loc5)
    (adjacent loc5 loc13)
    (adjacent loc13 loc5)
    (adjacent loc6 loc8)
    (adjacent loc8 loc6)
    (adjacent loc6 loc10)
    (adjacent loc10 loc6)
    (adjacent loc6 loc11)
    (adjacent loc11 loc6)
    (adjacent loc7 loc8)
    (adjacent loc8 loc7)
    (adjacent loc7 loc9)
    (adjacent loc9 loc7)
    (adjacent loc7 loc12)
    (adjacent loc12 loc7)
    (adjacent loc8 loc10)
    (adjacent loc10 loc8)
    (adjacent loc8 loc12)
    (adjacent loc12 loc8)
    (adjacent loc9 loc10)
    (adjacent loc10 loc9)
    (adjacent loc9 loc12)
    (adjacent loc12 loc9)
    (adjacent loc9 loc13)
    (adjacent loc13 loc9)
    (adjacent loc10 loc11)
    (adjacent loc11 loc10)
    (adjacent loc10 loc12)
    (adjacent loc12 loc10)
    (adjacent loc10 loc13)
    (adjacent loc13 loc10)
    (adjacent loc11 loc13)
    (adjacent loc13 loc11)
    (isHill loc11)
    (isHill loc8)
    (isHill loc9)
    (isHill loc7)
    (isHill loc3)
    (isHill loc10)
    (isWater loc6)
    (isWater loc4)
    (isWater loc12)
    (isWater loc2)
    (isWater loc5)
    (isGoal loc13)
  )

  (:goal (at loc13))

)