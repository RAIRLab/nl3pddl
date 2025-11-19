;; Solvable Hiking problem with water
;; Locations: 41, Hills: 10, Water: 10

(define (problem hiking-problem-41)
  (:domain hiking)

  (:objects
    loc1 - loc
    loc2 - loc
    loc3 - loc
    loc4 - loc
    loc5 - loc
    loc6 - loc
    loc7 - loc
    loc8 - loc
    loc9 - loc
    loc10 - loc
    loc11 - loc
    loc12 - loc
    loc13 - loc
    loc14 - loc
    loc15 - loc
    loc16 - loc
    loc17 - loc
    loc18 - loc
    loc19 - loc
    loc20 - loc
    loc21 - loc
    loc22 - loc
    loc23 - loc
    loc24 - loc
    loc25 - loc
    loc26 - loc
    loc27 - loc
    loc28 - loc
    loc29 - loc
    loc30 - loc
    loc31 - loc
    loc32 - loc
    loc33 - loc
    loc34 - loc
    loc35 - loc
    loc36 - loc
    loc37 - loc
    loc38 - loc
    loc39 - loc
    loc40 - loc
    loc41 - loc
  )

  (:init
    (at loc1)
    (adjacent loc1 loc2)
    (adjacent loc1 loc12)
    (adjacent loc2 loc1)
    (adjacent loc2 loc3)
    (adjacent loc3 loc2)
    (adjacent loc3 loc4)
    (adjacent loc4 loc3)
    (adjacent loc4 loc5)
    (adjacent loc4 loc25)
    (adjacent loc5 loc4)
    (adjacent loc5 loc6)
    (adjacent loc5 loc24)
    (adjacent loc6 loc5)
    (adjacent loc6 loc7)
    (adjacent loc7 loc6)
    (adjacent loc7 loc8)
    (adjacent loc7 loc24)
    (adjacent loc8 loc7)
    (adjacent loc8 loc9)
    (adjacent loc9 loc8)
    (adjacent loc9 loc10)
    (adjacent loc10 loc9)
    (adjacent loc10 loc11)
    (adjacent loc10 loc13)
    (adjacent loc11 loc10)
    (adjacent loc11 loc12)
    (adjacent loc11 loc15)
    (adjacent loc12 loc1)
    (adjacent loc12 loc11)
    (adjacent loc12 loc13)
    (adjacent loc12 loc36)
    (adjacent loc13 loc10)
    (adjacent loc13 loc12)
    (adjacent loc13 loc14)
    (adjacent loc14 loc13)
    (adjacent loc14 loc15)
    (adjacent loc15 loc11)
    (adjacent loc15 loc14)
    (adjacent loc15 loc16)
    (adjacent loc16 loc15)
    (adjacent loc16 loc17)
    (adjacent loc17 loc16)
    (adjacent loc17 loc18)
    (adjacent loc17 loc25)
    (adjacent loc18 loc17)
    (adjacent loc18 loc19)
    (adjacent loc18 loc39)
    (adjacent loc19 loc18)
    (adjacent loc19 loc20)
    (adjacent loc19 loc23)
    (adjacent loc19 loc35)
    (adjacent loc20 loc19)
    (adjacent loc20 loc21)
    (adjacent loc21 loc20)
    (adjacent loc21 loc22)
    (adjacent loc22 loc21)
    (adjacent loc22 loc23)
    (adjacent loc23 loc19)
    (adjacent loc23 loc22)
    (adjacent loc23 loc24)
    (adjacent loc23 loc37)
    (adjacent loc24 loc5)
    (adjacent loc24 loc7)
    (adjacent loc24 loc23)
    (adjacent loc24 loc25)
    (adjacent loc25 loc4)
    (adjacent loc25 loc17)
    (adjacent loc25 loc24)
    (adjacent loc25 loc26)
    (adjacent loc26 loc25)
    (adjacent loc26 loc27)
    (adjacent loc27 loc26)
    (adjacent loc27 loc28)
    (adjacent loc28 loc27)
    (adjacent loc28 loc29)
    (adjacent loc29 loc28)
    (adjacent loc29 loc30)
    (adjacent loc30 loc29)
    (adjacent loc30 loc31)
    (adjacent loc31 loc30)
    (adjacent loc31 loc32)
    (adjacent loc31 loc38)
    (adjacent loc32 loc31)
    (adjacent loc32 loc33)
    (adjacent loc32 loc37)
    (adjacent loc32 loc41)
    (adjacent loc33 loc32)
    (adjacent loc33 loc34)
    (adjacent loc34 loc33)
    (adjacent loc34 loc35)
    (adjacent loc35 loc19)
    (adjacent loc35 loc34)
    (adjacent loc35 loc36)
    (adjacent loc36 loc12)
    (adjacent loc36 loc35)
    (adjacent loc36 loc37)
    (adjacent loc37 loc23)
    (adjacent loc37 loc32)
    (adjacent loc37 loc36)
    (adjacent loc37 loc38)
    (adjacent loc38 loc31)
    (adjacent loc38 loc37)
    (adjacent loc38 loc39)
    (adjacent loc39 loc18)
    (adjacent loc39 loc38)
    (adjacent loc39 loc40)
    (adjacent loc40 loc39)
    (adjacent loc40 loc41)
    (adjacent loc41 loc32)
    (adjacent loc41 loc40)
    (isHill loc33)
    (isHill loc38)
    (isHill loc40)
    (isHill loc11)
    (isHill loc18)
    (isHill loc22)
    (isHill loc26)
    (isHill loc27)
    (isHill loc28)
    (isHill loc29)
    (isFlat loc2)
    (isFlat loc3)
    (isFlat loc4)
    (isFlat loc5)
    (isFlat loc6)
    (isFlat loc7)
    (isFlat loc8)
    (isFlat loc9)
    (isFlat loc10)
    (isFlat loc12)
    (isFlat loc13)
    (isFlat loc14)
    (isFlat loc15)
    (isFlat loc16)
    (isFlat loc17)
    (isFlat loc19)
    (isFlat loc20)
    (isFlat loc21)
    (isFlat loc23)
    (isFlat loc24)
    (isFlat loc25)
    (isFlat loc30)
    (isFlat loc31)
    (isFlat loc32)
    (isFlat loc34)
    (isFlat loc35)
    (isFlat loc36)
    (isFlat loc37)
    (isFlat loc39)
    (isFlat loc41)
    (isDry loc1)
    (isDry loc2)
    (isDry loc5)
    (isDry loc7)
    (isDry loc9)
    (isDry loc10)
    (isDry loc11)
    (isDry loc12)
    (isDry loc13)
    (isDry loc14)
    (isDry loc15)
    (isDry loc16)
    (isDry loc17)
    (isDry loc18)
    (isDry loc20)
    (isDry loc21)
    (isDry loc24)
    (isDry loc25)
    (isDry loc26)
    (isDry loc27)
    (isDry loc28)
    (isDry loc29)
    (isDry loc30)
    (isDry loc32)
    (isDry loc33)
    (isDry loc35)
    (isDry loc36)
    (isDry loc37)
    (isDry loc38)
    (isDry loc40)
    (isDry loc41)
  )

  (:goal (at loc41))
)
