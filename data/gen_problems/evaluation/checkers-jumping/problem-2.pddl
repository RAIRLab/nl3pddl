(define (problem checkers-jumping-prob-3)
  (:domain checkers-jumping)

  (:objects
    space1 space2 space3 space4 space5 space6 space7 - space
    red1 red2 red3 blue1 blue2 blue3 - checker
  )

  (:init
    (at red1 space1)
    (at red2 space2)
    (at red3 space3)
    (empty space4)
    (at blue1 space5)
    (at blue2 space6)
    (at blue3 space7)

    (right-of space1 space2)
    (right-of space2 space3)
    (right-of space3 space4)
    (right-of space4 space5)
    (right-of space5 space6)
    (right-of space6 space7)
    (left-of space2 space1)
    (left-of space3 space2)
    (left-of space4 space3)
    (left-of space5 space4)
    (left-of space6 space5)
    (left-of space7 space6)

    (is-red red1)
    (is-red red2)
    (is-red red3)
    (is-blue blue1)
    (is-blue blue2)
    (is-blue blue3)
  )

  (:goal (and
    (at blue1 space1)
    (at blue2 space2)
    (at blue3 space3)
    (empty space4)
    (at red1 space5)
    (at red2 space6)
    (at red3 space7)
  ))
)
