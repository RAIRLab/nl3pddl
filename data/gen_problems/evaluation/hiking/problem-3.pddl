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
    (adjacent loc1 loc2)
    (adjacent loc2 loc1)
    (adjacent loc1 loc4)
    (adjacent loc4 loc1)
    (adjacent loc1 loc5)
    (adjacent loc5 loc1)
    (adjacent loc2 loc4)
    (adjacent loc4 loc2)
    (adjacent loc4 loc5)
    (adjacent loc5 loc4)
    (adjacent loc4 loc6)
    (adjacent loc6 loc4)
    (adjacent loc5 loc7)
    (adjacent loc7 loc5)
    (isHill loc4)
    (isHill loc5)
    (isHill loc2)
    (isWater loc6)
    (isWater loc3)
    (isGoal loc7)
  )

  (:goal (at loc7))

)