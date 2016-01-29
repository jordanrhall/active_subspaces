import utils_analytic
import numpy as np
import active_subspaces
import matplotlib.pyplot as plt

# Set quantity of interest and input labels
QofI = 'U_avg'
in_labels = ['mu', 'rho', 'dpdx', 'eta', 'B0']

# Set the number of parameter (m) and active subspace dimension (n)
m, n = 5, 4

# Obtain M input samples drawn uniformly from the input space
M = 100
X_norm = 2*np.random.rand(M, m) - 1
X_phys = utils_analytic.normalized_to_physical(X=X_norm)

# Run simulation on sample inputs
f = utils_analytic.func(X_phys, QofI=QofI)
df_phys = utils_analytic.grad(X_phys, QofI=QofI)

# Scale data so parameters are in [-1,1]
df_norm = utils_analytic.physical_to_normalized(df=df_phys)

###############################################################################
##### Local Linear Approximation Gradients
###############################################################################

# Estimate gradients using local linear approximation
df_local_linear = active_subspaces.gradients.local_linear_gradients(X_phys, f)

# Scale data so parameters are in [-1,1]
df_local_linear = utils_analytic.physical_to_normalized(df=df_local_linear)

# Compute the active/inactive subspaces
# NOTE: The gradient is normalized for this computation
sub = active_subspaces.subspaces.Subspaces()
sub.compute(df_local_linear/np.linalg.norm(df_local_linear, axis=1).reshape((df_local_linear.shape[0], 1)))

# Rewrite the active/inactive subspace variables to be n-dimensional
sub.W1, sub.W2 = sub.eigenvectors[:,:n], sub.eigenvectors[:,n:]
sub.W1 = sub.W1.reshape(m, n)
sub.W2 = sub.W2.reshape(m, m-n)

# Define the active/inactive variables
Y, Z = np.dot(X_norm, sub.W1), np.dot(X_norm, sub.W2)

# Plot the active subspace info
active_subspaces.utils.plotters.eigenvalues(sub.eigenvalues, e_br=sub.e_br, out_label='Local Linear Approximation')
active_subspaces.utils.plotters.eigenvectors(sub.W1, in_labels=in_labels, out_label='Local Linear Approximation')

###############################################################################
##### Finite Difference Gradients
###############################################################################

# Estimate gradients using local linear approximation
df_fin_diff = active_subspaces.gradients.finite_difference_gradients(X_phys, utils_analytic.func)

# Scale data so parameters are in [-1,1]
df_fin_diff = utils_analytic.physical_to_normalized(df=df_fin_diff)

# Compute the active/inactive subspaces
# NOTE: The gradient is normalized for this computation
sub = active_subspaces.subspaces.Subspaces()
sub.compute(df_fin_diff/np.linalg.norm(df_fin_diff, axis=1).reshape((df_fin_diff.shape[0], 1)))

# Rewrite the active/inactive subspace variables to be n-dimensional
sub.W1, sub.W2 = sub.eigenvectors[:,:n], sub.eigenvectors[:,n:]
sub.W1 = sub.W1.reshape(m, n)
sub.W2 = sub.W2.reshape(m, m-n)

# Define the active/inactive variables
Y, Z = np.dot(X_norm, sub.W1), np.dot(X_norm, sub.W2)

# Plot the active subspace info
active_subspaces.utils.plotters.eigenvalues(sub.eigenvalues, e_br=sub.e_br, out_label='Finite Difference')
active_subspaces.utils.plotters.eigenvectors(sub.W1, in_labels=in_labels, out_label='Finite Difference')

###############################################################################
##### True Gradients
###############################################################################

# Compute the active/inactive subspaces
# NOTE: The gradient is normalized for this computation
sub = active_subspaces.subspaces.Subspaces()
sub.compute(df_norm/np.linalg.norm(df_norm, axis=1).reshape((M, 1)))

# Rewrite the active/inactive subspace variables to be n-dimensional
sub.W1, sub.W2 = sub.eigenvectors[:,:n], sub.eigenvectors[:,n:]
sub.W1 = sub.W1.reshape(m, n)
sub.W2 = sub.W2.reshape(m, m-n)

# Define the active/inactive variables
Y, Z = np.dot(X_norm, sub.W1), np.dot(X_norm, sub.W2)

# Plot the active subspace info
active_subspaces.utils.plotters.eigenvalues(sub.eigenvalues, e_br=sub.e_br, out_label='True')
active_subspaces.utils.plotters.eigenvectors(sub.W1, in_labels=in_labels, out_label='True')
