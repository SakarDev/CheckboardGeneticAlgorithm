# The Challenge:
- We are given an n by n checkerboard, in which every square can be one of four distinct colors.
- The goal is to arrange the colors on the checkerboard such that no two adjacent squares have the same color, considering only row-wise and column-wise adjacency (not diagonal).
- This repository accomplishes this task using a genetic algorithm.
<img alt="Checkboard example that is fixed using genetic algorithm" src="https://github.com/SakarDev/CheckboardGeneticAlgorithm/blob/master/checkboardExplanation.png" />

This AI project uses a genetic algorithm to optimally color a checkerboard, ensuring no adjacent color repetition, with results visualized as images.

# Code Explanation

1. Parameters: <b>error</b>, <b>size</b>, <b>samples</b>, <b>numberOfColors</b> are used to control the checkerboard's size, the number of samples, the number of colors, and to track errors. An initial population is created with <b>populations</b>, a 4x8x8 list of lists where each element is a random number between 0 and <b>numberOfColors</b>.

2. Helper functions:
<ul>
  <li> <b>printList3d</b> to print a 3D list.</li>
  <li><b>saveAsImages</b> to save checkerboards as images with different colors for visualization.</li>
  <li><b>calculateFitness</b> function computes the fitness of each sample in the population by counting the number of neighboring squares with the same color, a lower count signifies a better fitness.</li>
</ul>

3. The <b>calculateRowWise</b> and <b>calculateColWise</b> functions divide each of the best samples in half (either row-wise or column-wise) and calculate the fitness of these halves.

4. The <b>calculateHalfPartFitnessPerEachParent</b> function calls these functions for each of the best samples.

5. The <b>selectParent</b> function selects the best two samples as parents for the next generation.

6. The <b>crossover</b> function combines the best halves from the best samples to generate new samples. It includes row-wise and column-wise combinations.

7. The <b>columnWiseCombination</b> function is a helper for the <b>crossover</b> function, used for the column-wise combination.

8. The <b>mutation</b> function randomly changes a color in the checkerboard with a 10% probability, introducing variation.


