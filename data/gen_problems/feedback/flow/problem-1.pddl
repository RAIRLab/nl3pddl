
(define (problem flow_5_5) (:domain flow)
(:objects 
    c_1
	c_3
	c_4
	c_6
	c_5
	c_2 - color
    p_0_0
	p_0_1
	p_0_2
	p_0_3
	p_0_4
	p_1_0
	p_1_1
	p_1_2
	p_1_3
	p_1_4
	p_2_0
	p_2_1
	p_2_2
	p_2_3
	p_2_4
	p_3_0
	p_3_1
	p_3_2
	p_3_3
	p_3_4
	p_4_0
	p_4_1
	p_4_2
	p_4_3
	p_4_4 - location
)

(:init
    (offboard)
    (empty p_0_0)
	(empty p_0_1)
	(empty p_0_2)
	(empty p_0_3)
	(empty p_0_4)
	(empty p_1_0)
	(empty p_1_1)
	(empty p_1_2)
	(empty p_1_3)
	(empty p_1_4)
	(empty p_2_0)
	(empty p_2_1)
	(empty p_2_2)
	(empty p_2_3)
	(empty p_2_4)
	(empty p_3_0)
	(empty p_3_1)
	(empty p_3_2)
	(empty p_3_3)
	(empty p_3_4)
	(empty p_4_0)
	(empty p_4_1)
	(empty p_4_2)
	(empty p_4_3)
	(empty p_4_4)
    (adjacent p_0_0 p_1_0)
	(adjacent p_0_0 p_0_1)
	(adjacent p_0_1 p_1_1)
	(adjacent p_0_1 p_0_2)
	(adjacent p_0_1 p_0_0)
	(adjacent p_0_2 p_1_2)
	(adjacent p_0_2 p_0_3)
	(adjacent p_0_2 p_0_1)
	(adjacent p_0_3 p_1_3)
	(adjacent p_0_3 p_0_4)
	(adjacent p_0_3 p_0_2)
	(adjacent p_0_4 p_1_4)
	(adjacent p_0_4 p_0_3)
	(adjacent p_1_0 p_2_0)
	(adjacent p_1_0 p_1_1)
	(adjacent p_1_0 p_0_0)
	(adjacent p_1_1 p_2_1)
	(adjacent p_1_1 p_1_2)
	(adjacent p_1_1 p_0_1)
	(adjacent p_1_1 p_1_0)
	(adjacent p_1_2 p_2_2)
	(adjacent p_1_2 p_1_3)
	(adjacent p_1_2 p_0_2)
	(adjacent p_1_2 p_1_1)
	(adjacent p_1_3 p_2_3)
	(adjacent p_1_3 p_1_4)
	(adjacent p_1_3 p_0_3)
	(adjacent p_1_3 p_1_2)
	(adjacent p_1_4 p_2_4)
	(adjacent p_1_4 p_0_4)
	(adjacent p_1_4 p_1_3)
	(adjacent p_2_0 p_3_0)
	(adjacent p_2_0 p_2_1)
	(adjacent p_2_0 p_1_0)
	(adjacent p_2_1 p_3_1)
	(adjacent p_2_1 p_2_2)
	(adjacent p_2_1 p_1_1)
	(adjacent p_2_1 p_2_0)
	(adjacent p_2_2 p_3_2)
	(adjacent p_2_2 p_2_3)
	(adjacent p_2_2 p_1_2)
	(adjacent p_2_2 p_2_1)
	(adjacent p_2_3 p_3_3)
	(adjacent p_2_3 p_2_4)
	(adjacent p_2_3 p_1_3)
	(adjacent p_2_3 p_2_2)
	(adjacent p_2_4 p_3_4)
	(adjacent p_2_4 p_1_4)
	(adjacent p_2_4 p_2_3)
	(adjacent p_3_0 p_4_0)
	(adjacent p_3_0 p_3_1)
	(adjacent p_3_0 p_2_0)
	(adjacent p_3_1 p_4_1)
	(adjacent p_3_1 p_3_2)
	(adjacent p_3_1 p_2_1)
	(adjacent p_3_1 p_3_0)
	(adjacent p_3_2 p_4_2)
	(adjacent p_3_2 p_3_3)
	(adjacent p_3_2 p_2_2)
	(adjacent p_3_2 p_3_1)
	(adjacent p_3_3 p_4_3)
	(adjacent p_3_3 p_3_4)
	(adjacent p_3_3 p_2_3)
	(adjacent p_3_3 p_3_2)
	(adjacent p_3_4 p_4_4)
	(adjacent p_3_4 p_2_4)
	(adjacent p_3_4 p_3_3)
	(adjacent p_4_0 p_4_1)
	(adjacent p_4_0 p_3_0)
	(adjacent p_4_1 p_4_2)
	(adjacent p_4_1 p_3_1)
	(adjacent p_4_1 p_4_0)
	(adjacent p_4_2 p_4_3)
	(adjacent p_4_2 p_3_2)
	(adjacent p_4_2 p_4_1)
	(adjacent p_4_3 p_4_4)
	(adjacent p_4_3 p_3_3)
	(adjacent p_4_3 p_4_2)
	(adjacent p_4_4 p_3_4)
	(adjacent p_4_4 p_4_3)
    (flow-end p_0_1 c_1)
	(flow-end p_2_0 c_1)
	(flow-end p_0_2 c_3)
	(flow-end p_0_4 c_3)
	(flow-end p_1_2 c_4)
	(flow-end p_3_4 c_4)
	(flow-end p_1_3 c_6)
	(flow-end p_2_4 c_6)
	(flow-end p_2_2 c_5)
	(flow-end p_3_3 c_5)
	(flow-end p_3_0 c_2)
	(flow-end p_4_1 c_2)
)

(:goal (and
    ;We avoid using forall due to the translator implementation generating axioms which 
    ;make it so we can't use many good planner heuristics.
    ;(forall (?c - color) (flow-complete ?c))
    ;(forall (?l - location) (not-empty ?l))
    (flow-complete c_1)
	(flow-complete c_3)
	(flow-complete c_4)
	(flow-complete c_6)
	(flow-complete c_5)
	(flow-complete c_2)
    (not-empty p_0_0)
	(not-empty p_0_1)
	(not-empty p_0_2)
	(not-empty p_0_3)
	(not-empty p_0_4)
	(not-empty p_1_0)
	(not-empty p_1_1)
	(not-empty p_1_2)
	(not-empty p_1_3)
	(not-empty p_1_4)
	(not-empty p_2_0)
	(not-empty p_2_1)
	(not-empty p_2_2)
	(not-empty p_2_3)
	(not-empty p_2_4)
	(not-empty p_3_0)
	(not-empty p_3_1)
	(not-empty p_3_2)
	(not-empty p_3_3)
	(not-empty p_3_4)
	(not-empty p_4_0)
	(not-empty p_4_1)
	(not-empty p_4_2)
	(not-empty p_4_3)
	(not-empty p_4_4)
))

)