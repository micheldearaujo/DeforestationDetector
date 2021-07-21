# Performance Analysis of Machine Learning-Based Systems for Detecting Deforestation
## Combining Machine Learning with Drones to help protect Amazon Rainforest

This repository is meant to store my master's degree project files. This project main objetive is to analyze how does a low power computer (i.e a drone) supports running Machine Learning (ML) and Deep Learning (DL) algorithms to identify the land use and land cover of the Amazon rainforest.

Here is the timeline (without time) that i should follow

Train the following algorithms:

K-Nearest Neighbors (KNN);
Random Forest (RF);
Convolutional Neural Networks (CNN);
Recurrent Neural Networks (RNN);
All the algorithms must be trained for diverse images sizes for the sake of comparison if the image size afects the accuracy:

8x8;
16x16;
32x32;
64x64;
128x128;
After each algorithm is trained, it is time to make search for the best configurations for each one of them. This can be done;

KNN - Looking for the best number K;
RF - Looking for the best number of estimators;
CNN - Looking for the best threshold number;
RNN - i Don't know yet.
After choosen the best parameters of all the algorithms it is time to make single predictions on the raspiberry pi!

KNN;
RF;
CNN;
After all of this, comes the time to write everything down to the SMC paper!
