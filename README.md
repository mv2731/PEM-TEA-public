# PEM-TEA-private
Techno-economic analysis for proton exchange membranes. Private repo. 

In this README, we can add a description of the project or any project updates. In software engineering projects the README file typically serves as centralized documentation for the project. 

We can also create different branches depending on if we want to explore two different options from the same state of the code. Ie, if I wanted to compare whether factoring in degradation or factoring in renewable curtailment made more of a difference to our pricing, I could create two branches and work on implementing each in one branch.  

History on the upper left displays the commits made to a repository, and history is unique to each branch. 

Some relevant reading:
https://mg.readthedocs.io/git-jupyter.html

This says that it can be quite tedious to commit outputs of code cells:

"However, those cell outputs can be very annoying when using a version control system like e.g. Git. Whenever a change is made to a code cell, most likely the cell’s output will also change. The problem is that both changes will be shown in a “diff” view, but the (often much larger) changes in outputs will distract from the much more interesting changes in the code. This can make it very tedious to work on a notebook with multiple people."

But suggests a workaround that I can try to implement, creating a dev branch where we develop the notebooks, and a separate branch where we can commit notebooks with outputs displayed. 
