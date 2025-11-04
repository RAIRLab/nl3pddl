;; Hiking problem generator (solvable version)
;; Locations: 3, Hills: 1, Waters: 1, Seed: None

(define (problem hiking-problem-3-1-1)
  (:domain hiking)

  (:objects
    loc1 - loc
    loc2 - loc
    loc3 - loc
  )

  (:init
    (at loc1)
    (adjacent loc1 loc2)
    (adjacent loc1 loc3)
    (adjacent loc2 loc1)
    (adjacent loc2 loc3)
    (adjacent loc3 loc1)
    (adjacent loc3 loc2)
    (isHill loc2)
    (isGoal loc3)
  )

  (:goal (at loc3))
)
