import math
import re
import sympy as sp
from tabulate import tabulate

table_data = [ ["x", "f(x)", "f(x + h)", "f(x + 2h)", "f'(x) maju", "e(f)"] ]

expression = input("Input expression: ")
bottom_limit = float(input("Input bottom limit: "))
upper_limit = float(input("Input upper limit: "))

print("1. Forward Differential\n2. Integral")
choice = int(input("> "))

step = float(input(f"Input {"h" if choice == 1 else "n"}: "))

def preprocess(pattern):
    expression = pattern.replace("^", "**").replace("e", str(math.e))
    return re.sub(r'(-?\d)([a-zA-Z])', r'\1*\2', expression)

def evaluate_expression(expression, x_value):
    x = sp.Symbol('x')
    processed_expr = preprocess(expression)

    parsed_expr = sp.sympify(processed_expr)
    result = parsed_expr.subs(x, x_value).evalf()
    return result

def evaluate_differential(fxh, fx, h):
    return (fxh - fx) / h

def evaluate_error(fx2h, fxh, fx, h):
    return ( fx2h - (2 * fxh) + fx ) / ( 2 * h ) * -1

def do_differential():

    x = bottom_limit

    while x <= upper_limit:
        fx = evaluate_expression(expression, x)
        fxh = evaluate_expression(expression, x + step)
        fx2h = evaluate_expression(expression, x + 2 * step)
        error = evaluate_error(fx2h, fxh, fx, step)
        differential = evaluate_differential(fxh, fx, step)

        fx = round(fx, 8)
        fxh = round(fxh, 8)
        fx2h = round(fx2h, 8)
        error = round(error, 8)
        differential = round(differential, 8)

        table_data.append([x, fx, fxh, fx2h, differential, error])

        x += step

    print(tabulate(table_data, headers="firstrow", tablefmt="rounded_grid"))

def evaluate_integral(h, fxs):

    sums = 0

    for i in range(1, len(fxs) - 1):
        sums += fxs[i]

    result = h / 2 * ( (fxs[0] + 2 * sums + fxs[len(fxs) - 1]) )

    return result

def decimal_range(start, stop, increment):
    while start <= stop:
        yield start
        start += increment

def do_integral():
    h = (upper_limit - bottom_limit) / step
    fxs = [evaluate_expression(expression, x) for x in decimal_range(bottom_limit, upper_limit, h)]

    result = evaluate_integral(h, fxs)

    print(f"∫ f(x) dx from {bottom_limit} to {upper_limit} = {round(result, 3)}")

print()
print(f"f(x)\t= {preprocess(expression)}")
print(f"x\t= [{bottom_limit}, {upper_limit}]")
print(f"{"h" if choice == 1 else "n"}\t= {step}")

if choice == 1:
    do_differential()
elif choice == 2:
    do_integral()
else:
    print("Invalid input!")

