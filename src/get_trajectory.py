import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import pickle
import ast

# acceleration due to gravity constant
g = -9.80665

class Trajectory:

    def __init__(self):
        self.G = -9.81

    # applies a quadratic fit to position data to determine if trajectory is ballistic 
    # if confidence level > 0.9, return True

    def is_ballistic(data):

        # with open('trajectory-data', 'rb') as infile:
            # data = np.array(pickle.loads(infile))
            # data = np.array([ast.literal_eval(line) for line in fp if line.strip()])

        # print(data)
        # data = np.squeeze(data)
        # print(data, np.shape(data))
        
        t = [data[:,0]]
        X, Y, Z = [data[:,1][i] for i in range(4)]

        # print(X, np.shape(X))

        X = X.reshape(-1, 1)
        Y = Y.reshape(-1, 1)
        Z = Z.reshape(-1, 1)

        degree = 2  # Example: fit a 2nd-degree polynomial
        poly = PolynomialFeatures(degree=degree)
        X = np.concatenate((X, Y), axis=1) # Combine x and y coordinates
        X_poly = poly.fit_transform(X)

        model = LinearRegression()
        model.fit(X_poly, Z)

        z_predicted = model.predict(X_poly)

        # Calculate R-squared
        r2 = r2_score(Z, z_predicted)

        return r2 > 0.9
    
    def get_velocity_vector(self, pos, ts, t):

        x = pos[1][0]
        xc = pos[0][0]

        y = pos[1][1]
        yc = pos[0][1]

        z = pos[1][2]
        zc = pos[0][2]

        dxdt = (x-xc)/ts
        dydt = (y-yc)/ts
        dzdt = (z-zc)/ts

        return [dxdt, dydt, dzdt]

    def predict_position(self, pos, t, ts):

        dxdt, dydt, dzdt = self.get_velocity_vector(pos, ts, t)
        # assume no acceleration due to drag
        dvxdt = 0
        dvydt = 0
        dvydt = self.g

        sx = dxdt * t
        sy = dydt * t
        sz = (0.5 * dvydt * t**2) + (dzdt * t)

        return [sx, sy, sz]

    # TODO: take hardware into account (time of moving servo, dart reaching projectile, etc.)
    # def select_shot(timestep, model):
