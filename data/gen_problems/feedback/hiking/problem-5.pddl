;; Hiking problem generator (solvable version)
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
    (adjacent loc1 loc3)
    (adjacent loc1 loc4)
    (adjacent loc1 loc5)
    (adjacent loc1 loc6)
    (adjacent loc1 loc8)
    (adjacent loc1 loc11)
    (adjacent loc2 loc3)
    (adjacent loc2 loc4)
    (adjacent loc2 loc5)
    (adjacent loc2 loc6)
    (adjacent loc2 loc7)
    (adjacent loc3 loc1)
    (adjacent loc3 loc2)
    (adjacent loc3 loc7)
    (adjacent loc4 loc1)
    (adjacent loc4 loc2)
    (adjacent loc4 loc6)
    (adjacent loc4 loc8)
    (adjacent loc4 loc9)
    (adjacent loc5 loc1)
    (adjacent loc5 loc2)
    (adjacent loc5 loc6)
    (adjacent loc5 loc7)
    (adjacent loc5 loc8)
    (adjacent loc5 loc9)
    (adjacent loc6 loc1)
    (adjacent loc6 loc2)
    (adjacent loc6 loc4)
    (adjacent loc6 loc5)
    (adjacent loc6 loc7)
    (adjacent loc6 loc10)
    (adjacent loc7 loc2)
    (adjacent loc7 loc3)
    (adjacent loc7 loc5)
    (adjacent loc7 loc6)
    (adjacent loc7 loc9)
    (adjacent loc7 loc11)
    (adjacent loc8 loc1)
    (adjacent loc8 loc4)
    (adjacent loc8 loc5)
    (adjacent loc8 loc9)
    (adjacent loc8 loc10)
    (adjacent loc8 loc11)
    (adjacent loc9 loc4)
    (adjacent loc9 loc5)
    (adjacent loc9 loc7)
    (adjacent loc9 loc8)
    (adjacent loc10 loc6)
    (adjacent loc10 loc8)
    (adjacent loc10 loc11)
    (adjacent loc11 loc1)
    (adjacent loc11 loc7)
    (adjacent loc11 loc8)
    (adjacent loc11 loc10)
    (isHill loc3)
    (isHill loc6)
    (isHill loc8)
    (isHill loc9)
    (isHill loc10)
    (isGoal loc11)
  )

  (:goal (at loc11))
)
