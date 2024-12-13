import numpy as np
import matplotlib.pyplot as plt
import math

# Define the range for n
n = np.arange(1, 101)

# Define the functions
factorial = np.array([math.factorial(i) if i <= 20 else np.inf for i in n])  # Limit factorial growth for visualization
exponential = 2**n
polynomial = n**2
n_log_n = n * np.log2(n)
sqrt_n = np.sqrt(n)
log_n = np.log2(n)
constant = np.ones_like(n)

# Create the plot
plt.figure(figsize=(10, 8))

# Plot each function
plt.plot(n, factorial, 'k:', label=r"$n!$", linewidth=2)
plt.plot(n, exponential, 'r--', label=r"$2^n$", linewidth=2)
plt.plot(n, n_log_n, 'orange', label=r"$n \log_2 n$", linewidth=2)
plt.plot(n, polynomial, 'g-.', label=r"$n^2$", linewidth=2)
plt.plot(n, sqrt_n, 'b--', label=r"$\sqrt{n}$", linewidth=2)
plt.plot(n, log_n, 'm-.', label=r"$\log_2 n$", linewidth=2)
plt.plot(n, constant, 'purple', label=r"$1$", linewidth=2) 

# Set labels and title
plt.xlabel('n', fontsize=14)
plt.ylabel('N', fontsize=14)
plt.title('Growth Rates of Different Functions', fontsize=16)

# Set grid and axis limits
plt.grid(True)
plt.xlim(0, 100)
plt.ylim(0, 100)

# Add a legend
plt.legend()

# Show the plot
plt.show()
