;; Hiking problem generator (solvable version)
;; Locations: 7, Hills: 3, Waters: 3, Seed: None

(define (problem hiking-problem-7-3-3)
  (:domain hiking)

  (:objects
    loc1 - loc
    loc2 - loc
    loc3 - loc
    loc4 - loc
    loc5 - loc
    loc6 - loc
    loc7 - loc
  )

  (:init
    (at loc1)
    (adjacent loc1 loc2)
    (adjacent loc1 loc4)
    (adjacent loc1 loc6)
    (adjacent loc1 loc7)
    (adjacent loc2 loc1)
    (adjacent loc2 loc5)
    (adjacent loc2 loc6)
    (adjacent loc3 loc4)
    (adjacent loc3 loc5)
    (adjacent loc3 loc7)
    (adjacent loc4 loc1)
    (adjacent loc4 loc3)
    (adjacent loc4 loc6)
    (adjacent loc5 loc2)
    (adjacent loc5 loc3)
    (adjacent loc5 loc7)
    (adjacent loc6 loc1)
    (adjacent loc6 loc2)
    (adjacent loc6 loc4)
    (adjacent loc6 loc7)
    (adjacent loc7 loc1)
    (adjacent loc7 loc3)
    (adjacent loc7 loc5)
    (adjacent loc7 loc6)
    (isHill loc3)
    (isHill loc4)
    (isHill loc6)
    (isGoal loc7)
  )

  (:goal (at loc7))
)
