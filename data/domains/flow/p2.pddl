(define (problem flow_3_1) (:domain flow_free)
(:objects 
    red - color
    p_0_0
	p_1_0
	p_2_0 - location
)

(:init
    (offboard)
    (empty p_0_0)
	(empty p_1_0)
	(empty p_2_0)
    (adjacent p_0_0 p_1_0)
	(adjacent p_1_0 p_2_0)
	(adjacent p_1_0 p_0_0)
	(adjacent p_2_0 p_1_0)
    (flow-end p_0_0 red)
	(flow-end p_2_0 red)
)

(:goal (and
    ;(forall (?c - color) (flow-complete ?c))
    ;(forall (?l - location) (not-empty ?l))
    (flow-complete red)
    (not-empty p_0_0)
	(not-empty p_1_0)
	(not-empty p_2_0)
))

)