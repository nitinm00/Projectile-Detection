## Projectile Detection

This application mocks the operation of a missile/projectile defense system. It processes a live video feed and uses a trained neural network computer vision model to detect a red ball (our "projectile") in an image. 

It then calculates its position in three-dimensional space (since there is a single camera, we are using perspective geometry) and the angle needed to launch a toy bullet at it.
Once the algorithm can lock on and predict the projectile's trajectory, it instructs a servo-mounted toy gun to aim and shoot at the target.
