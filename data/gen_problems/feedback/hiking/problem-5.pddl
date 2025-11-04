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
    (adjacent loc1 loc2)
    (adjacent loc1 loc3)
    (adjacent loc1 loc8)
    (adjacent loc2 loc1)
    (adjacent loc2 loc4)
    (adjacent loc2 loc5)
    (adjacent loc2 loc7)
    (adjacent loc2 loc8)
    (adjacent loc2 loc10)
    (adjacent loc2 loc11)
    (adjacent loc3 loc1)
    (adjacent loc3 loc4)
    (adjacent loc3 loc5)
    (adjacent loc3 loc8)
    (adjacent loc3 loc9)
    (adjacent loc3 loc10)
    (adjacent loc3 loc11)
    (adjacent loc4 loc2)
    (adjacent loc4 loc3)
    (adjacent loc4 loc5)
    (adjacent loc4 loc7)
    (adjacent loc4 loc9)
    (adjacent loc4 loc10)
    (adjacent loc4 loc11)
    (adjacent loc5 loc2)
    (adjacent loc5 loc3)
    (adjacent loc5 loc4)
    (adjacent loc5 loc7)
    (adjacent loc5 loc9)
    (adjacent loc5 loc11)
    (adjacent loc6 loc7)
    (adjacent loc6 loc8)
    (adjacent loc6 loc11)
    (adjacent loc7 loc2)
    (adjacent loc7 loc4)
    (adjacent loc7 loc5)
    (adjacent loc7 loc6)
    (adjacent loc7 loc9)
    (adjacent loc7 loc10)
    (adjacent loc8 loc1)
    (adjacent loc8 loc2)
    (adjacent loc8 loc3)
    (adjacent loc8 loc6)
    (adjacent loc9 loc3)
    (adjacent loc9 loc4)
    (adjacent loc9 loc5)
    (adjacent loc9 loc7)
    (adjacent loc9 loc10)
    (adjacent loc9 loc11)
    (adjacent loc10 loc2)
    (adjacent loc10 loc3)
    (adjacent loc10 loc4)
    (adjacent loc10 loc7)
    (adjacent loc10 loc9)
    (adjacent loc11 loc2)
    (adjacent loc11 loc3)
    (adjacent loc11 loc4)
    (adjacent loc11 loc5)
    (adjacent loc11 loc6)
    (adjacent loc11 loc9)
    (isHill loc2)
    (isHill loc5)
    (isHill loc7)
    (isHill loc8)
    (isHill loc10)
    (isGoal loc11)
  )

  (:goal (at loc11))
)
