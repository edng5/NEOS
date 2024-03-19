# NEOS (Neuro Evolution Organism Simulator)
# by Edward Ng (2023)

> Original Copyright (c) 2017 Nathan Rooy

> Modified Copyright Edward Ng 2023

> Permission is hereby granted anyone is allowed to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software without charge.

An evolution simulator using NEAT algorithm. Tries to observe a population
of simple organisms (NEOS) learning to eat food. The NEOS can reproduce
within a generation to create offspring of shared genes. By the end of 
each generation sim, the fittest NEOS will carry the genes 
for the next generation.

The reproduction of NEOS is done through crossover and mutation of the two parents during intersection in the environemnt. Only individuals of high fitness are able to mate or 
else they will be rejected. In addition, once NEOS became too old they will die off. This poses possible obstacles to the success of the generation through spatial constraints, time, and elitism. 
In addition to mating within a generation, after each generation, the top 20% are selected in the population to create the next generation in the simulation.

It is observed that the average fitness greatly increases until generation 4 and drops off. At generation 6, the entire population dies off due to old age. The NEOS could have possibly reached a local optimum in terms 
of ability to eat food and once age and distance between fit individuals became too big, the ecosystem collapsed, leading to the end of the simulation.

# Experiment Results

Note: Due to being stochastic in nature, results are not always the same.

![](preview/gen_0.gif)

> GEN: 0 BEST: 42 AVG: 7.348837209302325 WORST: 2 SURVIVED: 20 DIED: 109 TOTAL NEOS: 129 FOOD EATEN: 948

![](preview/gen_1.gif)

> GEN: 1 BEST: 33 AVG: 10.512345679012345 WORST: 0 SURVIVED: 49 DIED: 113 TOTAL NEOS: 162 FOOD EATEN: 1703

![](preview/gen_2.gif)

> GEN: 2 BEST: 36 AVG: 12.13265306122449 WORST: 1 SURVIVED: 4 DIED: 94 TOTAL NEOS: 98 FOOD EATEN: 1189

![](preview/gen_3.gif)

> GEN: 3 BEST: 37 AVG: 11.094017094017094 WORST: 7 SURVIVED: 6 DIED: 111 TOTAL NEOS: 117 FOOD EATEN: 1298

![](preview/gen_4.gif)

> GEN: 4 BEST: 37 AVG: 13.336283185840708 WORST: 7 SURVIVED: 4 DIED: 109 TOTAL NEOS: 113 FOOD EATEN: 1507

![](preview/gen_5.gif)

> GEN: 5 BEST: 40 AVG: 11.627737226277372 WORST: 1 SURVIVED: 21 DIED: 116 TOTAL NEOS: 137 FOOD EATEN: 1593

![](preview/gen_6.gif)

> GEN 6 DID NOT SURVIVE...

> GEN: 6 BEST: 33 AVG: 12.518072289156626 WORST: 1 SURVIVED: 0 DIED: 83 TOTAL NEOS: 83 FOOD EATEN: 1039

