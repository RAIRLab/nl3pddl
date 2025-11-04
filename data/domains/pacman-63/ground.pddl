(define (domain pacman-63)
   (:requirements :strips :typing)
   (:types node)
   
   (:predicates
      (has_food ?location - node)
      (no_food ?location - node)
      (is_safe ?location - node)               ; complement of is_opponent_ghost
      (is_visited ?location - node)
      (at ?location - node)
      (not_at ?location - node)
      (connected ?n1 ?n2 - node)
   )

   (:action move_pacman
      :parameters (?start ?end - node)
      :precondition (and
         (at ?start)
         (not_at ?end)
         (no_food ?end)
         (connected ?start ?end)
         (is_safe ?end)
      )
      :effect (and
         (at ?end)
         (not_at ?start)
         (is_visited ?end)
      )
   )

   (:action eat_food
      :parameters (?start ?end - node)
      :precondition (and
         (at ?start)
         (has_food ?end)
         (connected ?start ?end)
         (is_safe ?end)
      )
      :effect (and
         (at ?end)
         (not_at ?start)
         (no_food ?end)
         (is_visited ?end)
      )
   )
)