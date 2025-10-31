; XXX
; XBXXXX
; XXXXXXXXX
;  XXXXXXXXX
;      XXGXX
;       XXX

(define (problem p01)
    (:domain bloxorz)
    ; t-r-c describes tile in row r column c
    ; 
    (:objects B - block
    t-01-01 t-01-02 t-01-03
    t-02-01 t-02-02 t-02-03 t-02-04 t-02-05 t-02-06
    t-03-01 t-03-02 t-03-03 t-03-04 t-03-05 t-03-06 t-03-07 t-03-08 t-03-09
    t-04-02 t-04-03 t-04-04 t-04-05 t-04-06 t-04-07 t-04-08 t-04-09 t-04-10 
    t-05-06 t-05-07 t-05-08 t-05-09 t-05-10
    t-06-07 t-06-08 t-06-09  - tile)

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

      (adjacent t-02-01 t-02-02 east)
      (adjacent t-02-02 t-02-03 east)
      (adjacent t-02-03 t-02-04 east)
      (adjacent t-02-04 t-02-05 east)
      (adjacent t-02-05 t-02-06 east)

      (adjacent t-03-01 t-03-02 east)
      (adjacent t-03-02 t-03-03 east)
      (adjacent t-03-03 t-03-04 east)
      (adjacent t-03-04 t-03-05 east)
      (adjacent t-03-05 t-03-06 east)
      (adjacent t-03-06 t-03-07 east)
      (adjacent t-03-07 t-03-08 east)
      (adjacent t-03-08 t-03-09 east)

      (adjacent t-04-02 t-04-03 east)
      (adjacent t-04-03 t-04-04 east)
      (adjacent t-04-04 t-04-05 east)
      (adjacent t-04-05 t-04-06 east)
      (adjacent t-04-06 t-04-07 east)
      (adjacent t-04-07 t-04-08 east)
      (adjacent t-04-08 t-04-09 east)
      (adjacent t-04-09 t-04-10 east)

      (adjacent t-05-06 t-05-07 east)
      (adjacent t-05-07 t-05-08 east)
      (adjacent t-05-08 t-05-09 east)
      (adjacent t-05-09 t-05-10 east)

      (adjacent t-06-07 t-06-08 east)
      (adjacent t-06-08 t-06-09 east)
      
      (adjacent t-01-01 t-02-01 south)
      (adjacent t-02-01 t-03-01 south)

      (adjacent t-01-02 t-02-02 south)
      (adjacent t-02-02 t-03-02 south)
      (adjacent t-03-02 t-04-02 south)

      (adjacent t-01-03 t-02-03 south)
      (adjacent t-02-03 t-03-03 south)
      (adjacent t-03-03 t-04-03 south)

      (adjacent t-02-04 t-03-04 south)
      (adjacent t-03-04 t-04-04 south)

      (adjacent t-02-05 t-03-05 south)
      (adjacent t-03-05 t-04-05 south)

      (adjacent t-02-06 t-03-06 south)
      (adjacent t-03-06 t-04-06 south)
      (adjacent t-04-06 t-05-06 south)

      (adjacent t-03-07 t-04-07 south)
      (adjacent t-04-07 t-05-07 south)
      (adjacent t-05-07 t-06-07 south)

      (adjacent t-03-08 t-04-08 south)
      (adjacent t-04-08 t-05-08 south)
      (adjacent t-05-08 t-06-08 south)

      (adjacent t-03-09 t-04-09 south)
      (adjacent t-04-09 t-05-09 south)
      (adjacent t-05-09 t-06-09 south)

      (adjacent t-04-10 t-05-10 south)


      (adjacent t-01-02 t-01-01 west)
      (adjacent t-01-03 t-01-02 west)

      (adjacent t-02-02 t-02-01 west)
      (adjacent t-02-03 t-02-02 west)
      (adjacent t-02-04 t-02-03 west)
      (adjacent t-02-05 t-02-04 west)
      (adjacent t-02-06 t-02-05 west)

      (adjacent t-03-02 t-03-01 west)
      (adjacent t-03-03 t-03-02 west)
      (adjacent t-03-04 t-03-03 west)
      (adjacent t-03-05 t-03-04 west)
      (adjacent t-03-06 t-03-05 west)
      (adjacent t-03-07 t-03-06 west)
      (adjacent t-03-08 t-03-07 west)
      (adjacent t-03-09 t-03-08 west)

      (adjacent t-04-03 t-04-02 west)
      (adjacent t-04-04 t-04-03 west)
      (adjacent t-04-05 t-04-04 west)
      (adjacent t-04-06 t-04-05 west)
      (adjacent t-04-07 t-04-06 west)
      (adjacent t-04-08 t-04-07 west)
      (adjacent t-04-09 t-04-08 west)
      (adjacent t-04-10 t-04-09 west)

      (adjacent t-05-07 t-05-06 west)
      (adjacent t-05-08 t-05-07 west)
      (adjacent t-05-09 t-05-08 west)
      (adjacent t-05-10 t-05-09 west)

      (adjacent t-06-08 t-06-07 west)
      (adjacent t-06-09 t-06-08 west)

      (adjacent t-02-01 t-01-01 north)
      (adjacent t-03-01 t-02-01 north)

      (adjacent t-02-02 t-01-02 north)
      (adjacent t-03-02 t-02-02 north)
      (adjacent t-04-02 t-03-02 north)

      (adjacent t-02-03 t-01-03 north)
      (adjacent t-03-03 t-02-03 north)
      (adjacent t-04-03 t-03-03 north)

      (adjacent t-03-04 t-02-04 north)
      (adjacent t-04-04 t-03-04 north)

      (adjacent t-03-05 t-02-05 north)
      (adjacent t-04-05 t-03-05 north)

      (adjacent t-03-06 t-02-06 north)
      (adjacent t-04-06 t-03-06 north)
      (adjacent t-05-06 t-04-06 north)

      (adjacent t-04-07 t-03-07 north)
      (adjacent t-05-07 t-04-07 north)
      (adjacent t-06-07 t-05-07 north)

      (adjacent t-04-08 t-03-08 north)
      (adjacent t-05-08 t-04-08 north)
      (adjacent t-06-08 t-05-08 north)

      (adjacent t-04-09 t-03-09 north)
      (adjacent t-05-09 t-04-09 north)
      (adjacent t-06-09 t-05-09 north)

      (adjacent t-05-10 t-04-10 north)

      (standing-on B t-02-02)
    )


    (:goal (and 
      (standing-on B t-05-08)
    ))
)