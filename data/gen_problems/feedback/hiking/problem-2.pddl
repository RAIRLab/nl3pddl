;; Hiking problem generator (solvable version)
;; Locations: 5, Hills: 2, Waters: 2, Seed: None

(define (problem hiking-problem-5-2-2)
  (:domain hiking)

  (:objects
    loc1 - loc
    loc2 - loc
    loc3 - loc
    loc4 - loc
    loc5 - loc
  )

  (:init
    (at loc1)
    (adjacent loc1 loc2)
    (adjacent loc1 loc3)
    (adjacent loc1 loc5)
    (adjacent loc2 loc1)
    (adjacent loc2 loc3)
    (adjacent loc2 loc4)
    (adjacent loc3 loc1)
    (adjacent loc3 loc2)
    (adjacent loc3 loc4)
    (adjacent loc3 loc5)
    (adjacent loc4 loc2)
    (adjacent loc4 loc3)
    (adjacent loc4 loc5)
    (adjacent loc5 loc1)
    (adjacent loc5 loc3)
    (adjacent loc5 loc4)
    (isHill loc3)
    (isHill loc4)
    (isGoal loc5)
  )

  (:goal (at loc5))
)
