# Wikipedia-Hitler-Game

Play the popular and amusing Wikipedia Hitler Game, but let the computer do it for you!

### Game rules:
1. Start from a random Wikipedia page
2. Click on links in that article to get to other articles, until you open Hitler's Wikipedia page

### Implementation:
This simple implementation in Python 2 finds the optimal solution (minumum number of links) with a breadth-first search (it might be slow!)

### Usage:
For a more politically correct game, you can change the target final link

![Screenshot](doc/usage.png?raw=true)

### Example of the program running:
![Screenshot](doc/example.png?raw=true)

### Future improvements:
* Parallel downloading of web pages
* Heuristic in order to look first to the link that might lead to the target one
    - Ideas: train a neural network on the target web page in order to recognize the most correlated words


Wrote this for fun in 2 hours
