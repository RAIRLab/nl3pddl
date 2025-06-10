(define (domain alchemy)
  (:requirements :strips :typing)
  
  (:types
      alchemist ingredient container potion - object
  )
  
  (:predicates
    (available ?i - ingredient)
    (has-ingredient ?a - alchemist ?i - ingredient)
    (in ?i - ingredient ?c - container)  
    (mixture-complete ?c - container)    
    (potion-ready ?p - potion ?c - container) 
    (different ?i1 ?i2 - ingredient)
  )
  
  (:action collect-ingredient
    :parameters (?a - alchemist ?i - ingredient)
    :precondition (available ?i)
    :effect (and (has-ingredient ?a ?i) (not (available ?i)))
  )

  (:action add-ingredient
    :parameters (?a - alchemist ?i - ingredient ?c - container)
    :precondition (has-ingredient ?a ?i)
    :effect (and (in ?i ?c) (not (has-ingredient ?a ?i)))
  )
  
  (:action clean-container
    :parameters (?a - alchemist ?c - container ?i - ingredient)
    :precondition (in ?i ?c)
    :effect (not (in ?i ?c))
  )
  
  (:action mix-ingredients
    :parameters (?a - alchemist ?r1 ?r2 ?r3 - ingredient ?c - container)
    :precondition (and (in ?r1 ?c) (in ?r2 ?c) (in ?r3 ?c) (different ?r1 ?r2) (different ?r1 ?r3) (different ?r2 ?r3))
    :effect (and (mixture-complete ?c))
  )
  
  (:action brew-potion
    :parameters (?a - alchemist ?c - container ?p - potion)
    :precondition (mixture-complete ?c)
    :effect (potion-ready ?p ?c)
  )
)
