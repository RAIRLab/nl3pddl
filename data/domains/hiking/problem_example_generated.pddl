;; Hiking problem generator
;; Locations: 6, Hills: 2, Waters: 1, Seed: 42
(define (problem hiking-problem-6-2-1)
  (:domain hiking)
  (:objects
    loc1 - loc
    loc2 - loc
    loc3 - loc
    loc4 - loc
    loc5 - loc
    loc6 - loc
  )
  (:init
    (at loc1)
    (adjacent loc1 loc3)
    (adjacent loc3 loc1)
    (adjacent loc1 loc4)
    (adjacent loc4 loc1)
    (adjacent loc1 loc5)
    (adjacent loc5 loc1)
    (adjacent loc2 loc5)
    (adjacent loc5 loc2)
    (adjacent loc2 loc6)
    (adjacent loc6 loc2)
    (adjacent loc3 loc4)
    (adjacent loc4 loc3)
    (adjacent loc3 loc5)
    (adjacent loc5 loc3)
    (adjacent loc4 loc5)
    (adjacent loc5 loc4)
    (adjacent loc4 loc6)
    (adjacent loc6 loc4)
    (isHill loc4)
    (isHill loc3)
    (isWater loc2)
    (isGoal loc6)
  )
  (:goal (at loc6))
)
