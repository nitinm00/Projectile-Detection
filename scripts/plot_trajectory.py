import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import pickle
import ast

with open('trajectory-data', 'rb') as infile:
    # data = np.array(pickle.loads(infile))
    data = np.array([ast.literal_eval(line) for line in fp if line.strip()])

    # print(data)
data = np.squeeze(data)
# print(data, np.shape(data))

X, Y, Z = [data[:,i] for i in range(3)]

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

# print("r2 score:",r2)

# # Create a 3D plot
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# # Plot the trajectory
# ax.plot(X, Y, Z, label="Ball Trajectory", color="blue", marker="o", markersize=3)

# # Add labels and title
# ax.set_xlabel("X (meters)")
# ax.set_ylabel("Y (meters)")
# ax.set_zlabel("Z (meters)")
# ax.set_title("3D Trajectory of the Ball")

# # Add a legend
# ax.legend()
# plt.axis('equal')
# # Show the plot
# plt.show()