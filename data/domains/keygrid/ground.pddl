(define (domain grid)
  (:requirements :strips :typing)


  ;; ADDED TO THE ORIGINAL PDDL 
  (:types place key shape)
  ;; ADDED TO THE ORIGINAL PDDL END

  (:predicates 
    (conn ?x ?y) 
    (key-shape ?k ?s) 
    (lock-shape ?x ?s)
    (at ?r ?x ) 
    (at-robot ?x) 
    (place ?p) 
    (key ?k) 
    (shape ?s)
	  (locked ?x) 
    (holding ?k)  
    (open ?x)  
    (arm-empty)
  )

  (:action unlock
    :parameters (?curpos ?lockpos - place ?key - key ?shape - shape)
    :precondition (and
      (conn ?curpos ?lockpos)
		  (key-shape ?key ?shape) 
      (lock-shape ?lockpos ?shape)
		  (at-robot ?curpos) 
      (locked ?lockpos) 
      (holding ?key))
    :effect (and (open ?lockpos) (not (locked ?lockpos))))

  (:action move
    :parameters (?curpos ?nextpos - place)
    :precondition (and (at-robot ?curpos)
		       (conn ?curpos ?nextpos) (open ?nextpos))
    :effect (and (at-robot ?nextpos) (not (at-robot ?curpos))))

  (:action pickup
    :parameters (?curpos - place ?key - key)
    :precondition (and (at-robot ?curpos)
		       (at ?key ?curpos) (arm-empty ))
    :effect (and (holding ?key) (not (at ?key ?curpos)) (not (arm-empty ))))

  (:action pickup-and-loose
    :parameters (?curpos - place ?newkey - key ?oldkey - key)
    :precondition (and (at-robot ?curpos) (holding ?oldkey)
		       (at ?newkey ?curpos))
    :effect (and (holding ?newkey) (at ?oldkey ?curpos)
		 (not (holding ?oldkey)) (not (at ?newkey ?curpos))))

  (:action putdown
    :parameters (?curpos - place ?key - key)
    :precondition (and (at-robot ?curpos) (holding ?key))
    :effect (and (arm-empty) (at ?key ?curpos) (not (holding ?key))))
  )
