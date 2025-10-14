(define (domain pacman-63)
   (:requirements :strips :typing)
   (:types node)
   
   (:predicates
      (has_food ?location - node)
      (no_food ?location - node)          ; complement of has_food
      (is_opponent_ghost ?location - node)
      (is_visited ?location)
      (at ?location - node)
      (not_at ?location - node)           ; complement of at
      (connected ?n1 ?n2 - node)
   )

   (:action move_pacman 
      :parameters (?start ?end - node)
      :precondition (and
         (at ?start)
         (not_at ?end)
         (no_food ?end)
         (connected ?start ?end)
         (not (is_opponent_ghost ?end))
      )
      :effect (and
         (not (at ?start))
         (at ?end)
         (not_at ?start)
         (not (not_at ?end))
         (is_visited ?end)
      )
   )

   (:action eat_food
      :parameters (?start ?end - node)
      :precondition (and
         (at ?start)
         (has_food ?end)
         (connected ?start ?end)
         (not (is_opponent_ghost ?end))
      )
      :effect (and
         (at ?end)
         (not (at ?start))
         (not_at ?start)
         (not (no_food ?end))
         (no_food ?end)
         (not (has_food ?end))
         (is_visited ?end)
      )
   )
)