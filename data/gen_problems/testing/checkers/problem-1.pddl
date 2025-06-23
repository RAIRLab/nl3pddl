(define (problem checkers-jumping-prob-2)
  (:domain checkers-jumping)

  (:objects
    space1 space2 space3 space4 space5 - space
    red1 red2 blue1 blue2 - checker
  )

  (:init
    (at red1 space1)
    (at red2 space2)
    (empty space3)
    (at blue1 space4)
    (at blue2 space5)

    (right-of space1 space2)
    (right-of space2 space3)
    (right-of space3 space4)
    (right-of space4 space5)
    (left-of space2 space1)
    (left-of space3 space2)
    (left-of space4 space3)
    (left-of space5 space4)

    (is-red red1)
    (is-red red2)
    (is-blue blue1)
    (is-blue blue2)
  )

  (:goal (and
    (at blue1 space1)
    (at blue2 space2)
    (empty space3)
    (at red1 space4)
    (at red2 space5)
  ))
)
