(define (domain KnightTour)
  (:requirements :strips :typing)
  (:types pos)
  
  (:predicates
    (at ?col ?row - pos)

    (visited ?col ?row - pos)

    (unvisited ?col ?row - pos)
    
    (increase_one ?x ?y - pos)
    (increase_two ?x ?y - pos)
  )

  (:action move_2col_1row
    :parameters (?from_col ?from_row ?to_col ?to_row - pos)
    :precondition (and
       (at ?from_col ?from_row)
       (increase_two ?from_col ?to_col)
       (increase_one ?from_row ?to_row)
       (unvisited ?to_col ?to_row)
    )
    :effect (and
       (not (at ?from_col ?from_row))
       (at ?to_col ?to_row)
       (not (unvisited ?to_col ?to_row))
       (visited ?to_col ?to_row)
    )
  )

  (:action move_2row_1col
    :parameters (?from_col ?from_row ?to_col ?to_row - pos)
    :precondition (and
       (at ?from_col ?from_row)
       (increase_two ?from_row ?to_row)
       (increase_one ?from_col ?to_col)
       (unvisited ?to_col ?to_row)
    )
    :effect (and
       (not (at ?from_col ?from_row))
       (at ?to_col ?to_row)
       (not (unvisited ?to_col ?to_row))
       (visited ?to_col ?to_row)
    )
  )
)
