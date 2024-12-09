import sympy as sp
import matplotlib.pyplot as plt
import numpy as np

def find_asymptotes(expr):
    x = sp.symbols('x')
    f = sp.sympify(expr)

    # Find vertical asymptotes
    vertical_asymptotes = sp.solve(sp.denom(f), x)

    # Find horizontal asymptotes
    horizontal_asymptote = sp.limit(f, x, sp.oo)

    # Find oblique asymptotes
    oblique_asymptote = None
    if horizontal_asymptote == sp.oo or horizontal_asymptote == -sp.oo:
        oblique_asymptote = sp.limit(f/x, x, sp.oo) * x

    return vertical_asymptotes, horizontal_asymptote, oblique_asymptote

def plot_function_and_asymptotes(expr):
    x = sp.symbols('x')
    f = sp.sympify(expr)
    vertical_asymptotes, horizontal_asymptote, oblique_asymptote = find_asymptotes(expr)

    # Convert sympy function to numpy function
    f_lambdified = sp.lambdify(x, f, modules=['numpy'])

    # Generate x values
    x_vals = np.linspace(-10, 10, 400)
    y_vals = f_lambdified(x_vals)

    plt.figure(figsize=(10, 6))
    plt.plot(x_vals, y_vals, label=f'f(x) = {expr}')

    # Plot vertical asymptotes
    for va in vertical_asymptotes:
        plt.axvline(x=va, color='r', linestyle='--', label=f'Vertical Asymptote: x = {va}')

    # Plot horizontal asymptote
    if horizontal_asymptote != sp.oo and horizontal_asymptote != -sp.oo:
        plt.axhline(y=horizontal_asymptote, color='g', linestyle='--', label=f'Horizontal Asymptote: y = {horizontal_asymptote}')

    # Plot oblique asymptote
    if oblique_asymptote:
        oblique_asymptote_lambdified = sp.lambdify(x, oblique_asymptote, modules=['numpy'])
        y_oblique_vals = oblique_asymptote_lambdified(x_vals)
        plt.plot(x_vals, y_oblique_vals, color='b', linestyle='--', label=f'Oblique Asymptote: y = {oblique_asymptote}')

    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('Function and Asymptotes')
    plt.legend()
    plt.grid(True)
    plt.ylim(-10, 10)
    plt.xlim(-10, 10)
    plt.show()

def main():
    expr = '(3*x**2 - 1) / (x**2 + 2*x)'
    vertical_asymptotes, horizontal_asymptote, oblique_asymptote = find_asymptotes(expr)

    print(f"Function: {expr}")
    print(f"Vertical Asymptotes: {vertical_asymptotes}")
    print(f"Horizontal Asymptote: {horizontal_asymptote}")
    if oblique_asymptote:
        print(f"Oblique Asymptote: {oblique_asymptote}")

    plot_function_and_asymptotes(expr)

if __name__ == "__main__":
    main()