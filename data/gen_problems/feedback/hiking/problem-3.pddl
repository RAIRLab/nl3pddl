;; Hiking problem generator
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
    (adjacent loc1 loc3)
    (adjacent loc3 loc1)
    (adjacent loc1 loc4)
    (adjacent loc4 loc1)
    (adjacent loc1 loc5)
    (adjacent loc5 loc1)
    (adjacent loc1 loc7)
    (adjacent loc7 loc1)
    (adjacent loc2 loc4)
    (adjacent loc4 loc2)
    (adjacent loc2 loc5)
    (adjacent loc5 loc2)
    (adjacent loc2 loc7)
    (adjacent loc7 loc2)
    (adjacent loc3 loc6)
    (adjacent loc6 loc3)
    (adjacent loc4 loc6)
    (adjacent loc6 loc4)
    (adjacent loc4 loc7)
    (adjacent loc7 loc4)
    (isHill loc5)
    (isHill loc3)
    (isHill loc4)
    (isWater loc6)
    (isWater loc2)
    (isGoal loc7)
  )

  (:goal (at loc7))

)