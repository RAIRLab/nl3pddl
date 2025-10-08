(define (domain pacman_ai)
   (:requirements :typing)
   (:types node)
   (:predicates
            (has_food ?location -node)
            (is_opponent_ghost ?location -node)
            (is_opponent_pacman ?location -node)
            (is_visited ?location)
            (at ?location - node)
            (connected ?n1 ?n2 - node)
            (eat_food ?start ?end -node)
            (move_pacman ?start ?end -node)
            (move_ghost ?start ?end -node)
            (eat_pacman ?start ?end -node)

	       )
    (:action move_pacman 
         :parameters (?start ?end -node)
         :precondition (
         and
         (at ?start)
         (not (has_food ?end))
         (connected ?start ?end)
         (not (is_opponent_ghost ?end))
         )
         :effect (and
         (not (at ?start))
         (at ?end)
         (is_visited ?end)
         )

      )
    (:action eat_food
        :parameters (?start ?end -node)
        :precondition (
        and
        (at ?start)
        (has_food ?end)
        (connected ?start ?end)
        (not (is_opponent_ghost ?end))
        )
        :effect (and
        (at ?end)
        (not (at ?start))
        (not (has_food ?end))
        (is_visited ?end)
        )

     )

)