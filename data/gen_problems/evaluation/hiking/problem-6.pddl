;; Hiking problem generator (solvable version)
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
    (adjacent loc1 loc4)
    (adjacent loc1 loc6)
    (adjacent loc1 loc8)
    (adjacent loc2 loc1)
    (adjacent loc2 loc4)
    (adjacent loc2 loc6)
    (adjacent loc2 loc7)
    (adjacent loc2 loc13)
    (adjacent loc3 loc7)
    (adjacent loc3 loc10)
    (adjacent loc3 loc12)
    (adjacent loc4 loc1)
    (adjacent loc4 loc2)
    (adjacent loc4 loc9)
    (adjacent loc4 loc10)
    (adjacent loc4 loc11)
    (adjacent loc5 loc6)
    (adjacent loc5 loc7)
    (adjacent loc5 loc8)
    (adjacent loc5 loc9)
    (adjacent loc6 loc1)
    (adjacent loc6 loc2)
    (adjacent loc6 loc5)
    (adjacent loc6 loc7)
    (adjacent loc6 loc8)
    (adjacent loc6 loc11)
    (adjacent loc6 loc12)
    (adjacent loc7 loc2)
    (adjacent loc7 loc3)
    (adjacent loc7 loc5)
    (adjacent loc7 loc6)
    (adjacent loc7 loc11)
    (adjacent loc7 loc12)
    (adjacent loc8 loc1)
    (adjacent loc8 loc5)
    (adjacent loc8 loc6)
    (adjacent loc8 loc10)
    (adjacent loc8 loc12)
    (adjacent loc9 loc4)
    (adjacent loc9 loc5)
    (adjacent loc9 loc13)
    (adjacent loc10 loc3)
    (adjacent loc10 loc4)
    (adjacent loc10 loc8)
    (adjacent loc10 loc11)
    (adjacent loc10 loc13)
    (adjacent loc11 loc4)
    (adjacent loc11 loc6)
    (adjacent loc11 loc7)
    (adjacent loc11 loc10)
    (adjacent loc11 loc12)
    (adjacent loc11 loc13)
    (adjacent loc12 loc3)
    (adjacent loc12 loc6)
    (adjacent loc12 loc7)
    (adjacent loc12 loc8)
    (adjacent loc12 loc11)
    (adjacent loc13 loc2)
    (adjacent loc13 loc9)
    (adjacent loc13 loc10)
    (adjacent loc13 loc11)
    (isHill loc2)
    (isHill loc3)
    (isHill loc4)
    (isHill loc7)
    (isHill loc8)
    (isHill loc11)
    (isGoal loc13)
  )

  (:goal (at loc13))
)
