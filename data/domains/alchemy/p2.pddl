(define (problem alchemy-p1)
  (:domain alchemy)
  
  (:objects
    herb - ingredient
    mushroom - ingredient
    crystal - ingredient
    sapphire - ingredient
    alchemist1 - alchemist
    container1 - container
    potion1 - potion
  )
  
  (:init
    ;; The three required ingredients are available.
    (available herb)
    (available mushroom)
    (available crystal)
    (available sapphire)
    (different herb mushroom)
    (different herb sapphire)
    (different mushroom crystal)
    (different mushroom herb)
    (different crystal herb)
    (different crystal mushroom)
  )
  
  (:goal
    ;; The goal is for the potion to be brewed in the container.
    (potion-ready potion1 container1)
  )
)