(define (problem hiking-problem-human)
  (:domain hiking)

  (:objects
    start hill1 flat1 goal - loc
  )

  (:init
    ;; current location
    (at start)

    ;; map connections
    (adjacent start flat1)
    (adjacent flat1 start)
    (adjacent flat1 hill1)
    (adjacent hill1 flat1)
    (adjacent hill1 goal)
    (adjacent goal hill1)

    ;; terrain features
    (isHill hill1)
    (isGoal goal)
    ;; note: no water locations here
  )

  
  (:goal (at goal))
  
)