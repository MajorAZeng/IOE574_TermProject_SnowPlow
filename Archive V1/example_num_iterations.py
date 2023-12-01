num_simulations = 1000

# Half-width of the confidence interval
D = 0.001

parameters = [(-0.1, 10, 5), (-0.5, 15, 2), (-1.0, 20, 1)]

def calculate_iterations(variance, half_width):
    z_score = norm.ppf(0.975)
    required_iterations = (variance * z_score**2) / (half_width**2)
    return np.ceil(required_iterations)  # Rounding up to the nearest whole number

# Run simulations and calculate mean and variance for each set of parameters
for mu, A, B in parameters:
    estimates = importance_sampling(mu, A, B, num_simulations)
    print(estimates)
    mean_estimate = np.mean(estimates)
    variance_estimate = np.var(estimates)
    iterations_needed = calculate_iterations(variance_estimate, D)
    print(f"Mean of estimates for mu={mu}, A={A}, B={B}: {mean_estimate}")
    print(f"Variance of estimates for mu={mu}, A={A}, B={B}: {variance_estimate}")
    print(f"Number of iterations needed: {iterations_needed}")
    
from scipy.stats import norm

# Calculate the z-value for the 97.5th percentile
z_0_975 = norm.ppf(0.975)
print(f"z_0.975 value: {z_0_975}")
