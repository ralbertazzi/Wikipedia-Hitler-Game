# Wikipedia-Hitler-Game

Play the popular and amusing Wikipedia Hitler Game, but let the computer do it for you!

### Game rules:
1. Start from a random Wikipedia page
2. Click on links in that article to get to other articles, until you open Hitler's Wikipedia page

### Implementation:
This simple implementation in Python 2 finds the optimal solution (minumum number of links) with a breadth-first search (it might be slow!)

Update 2018/01/12: implemented multiprocessing version (more processes -> parallel downloading of web pages).
Italy -> Adolf_Hitler takes 19s instead of 43s. Python_(programming_language) takes 10min 30s instead of 24min.

### Usage:
For a more politically correct game, you can change the target final link

![Screenshot](doc/usage.png?raw=true)

### Example of the program running:
![Screenshot](doc/example.png?raw=true)

### Future improvements:
* Heuristic in order to look first to the link that might lead to the target one
    - Ideas: train a neural network on the target web page in order to recognize the most correlated words


Wrote this for fun in 2 hours
