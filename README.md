# tv-show-recommender

Get television show recommendations based on the shows you already like.

## Context

This project will serve primarily as a learning experience for me. 
I am interested in adding basic machine learning competency to my toolbelt and am particularly interested in MLOps.

My goals are:
* Acquire a good enough data set for training a machine learning model
* Train a good enough model using said data set
* Serve the model embedded in a web application with an interface
* Automate the deployment, monitoring, and re-training of the model such that we never introduce regressions nor does the model rot
* Not have to have a family crisis whenever the show my spouse and I are invested in is close to ending

My stretch goals are:
* Displaying an interactive graphical visualization (literally) of the shows people like
* Training the model such that it accounts for recency, e.g., if a hot new show comes out, the model shouldn't take too long to add that to its corpus.