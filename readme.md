# Killdozer
A pathfinding and routing algorithm to determine the best path of destruction. Created by Daniel Slade, Joe Moules, and Abegail Palad for CMPE185 - Autonomous Mobile Robots

# How to Use
This application uses pygame for graphics, so make sure to install pygame using `pip install pygame`.
The application also requires a video driver, so it cannot be run purely on terminal. The easiest
way to use the application is to put the code in an IDE such as PyCharm and run. \
\
To set up the buildings, dimensions, and depth for searching for routing, edit setup.json.
setting `FILE` to "random" will randomly generate a town. To create a custom town, make a folder
that has `start.txt`, `targets.txt`, and`avoids.txt`. Format for these folders can be seen in `sampleInput`.
To use the folder, set `FILE` in setup.json to the name of the folder. The value of `SEARCHDEPTH` should be considered
based on how many target buildings there are. If computing a path takes too long, lower `SEARCHDEPTH`.