; XXXX
; BXGX
;  XXX

(define (problem p02)
    (:domain bloxorz)
    ; t-r-c describes tile in row r column c
    ; 
    (:objects B - block
    t-01-01 t-01-02 t-01-03 t-01-04
    t-02-01 t-02-02 t-02-03 t-02-04
    t-03-02 t-03-03 t-03-04 - tile)

    (:init
      (perpendicular north east)
      (perpendicular north west)
      (perpendicular east north)
      (perpendicular west north)
      (perpendicular south east)
      (perpendicular south west)
      (perpendicular east south)
      (perpendicular west south)

      (adjacent t-01-01 t-01-02 east)
      (adjacent t-01-02 t-01-03 east)
      (adjacent t-01-03 t-01-04 east)

      (adjacent t-02-01 t-02-02 east)
      (adjacent t-02-02 t-02-03 east)
      (adjacent t-02-03 t-02-04 east)

      (adjacent t-03-02 t-03-03 east)
      (adjacent t-03-03 t-03-04 east)
   

      
      (adjacent t-01-01 t-02-01 south)

      (adjacent t-01-02 t-02-02 south)
      (adjacent t-02-02 t-03-02 south)

      (adjacent t-01-03 t-02-03 south)
      (adjacent t-02-03 t-03-03 south)

      (adjacent t-01-04 t-02-04 south)
      (adjacent t-02-04 t-03-04 south)



      (adjacent t-01-02 t-01-01 west)
      (adjacent t-01-03 t-01-02 west)
      (adjacent t-01-04 t-01-03 west)

      (adjacent t-02-02 t-02-01 west)
      (adjacent t-02-03 t-02-02 west)
      (adjacent t-02-04 t-02-03 west)

      (adjacent t-03-03 t-03-02 west)
      (adjacent t-03-04 t-03-03 west)



      (adjacent t-02-01 t-01-01 north)

      (adjacent t-02-02 t-01-02 north)
      (adjacent t-03-02 t-02-02 north)

      (adjacent t-02-03 t-01-03 north)
      (adjacent t-03-03 t-02-03 north)

      (adjacent t-02-04 t-01-04 north)
      (adjacent t-03-04 t-02-04 north)


      (standing-on B t-02-01)
    )


    (:goal (and 
      (standing-on B t-02-03)
    ))
)