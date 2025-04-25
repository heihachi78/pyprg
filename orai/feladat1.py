input_integer = input("Please enter an integer: ")

def prime_factors(n):
    factors = []
    i = 2
    while i <= n:
        if n % i == 0:
            factors.append(i)
            n = n // i
        else:
            i += 1
    return factors

if input_integer.isdigit():
    print("The input is an integer.")
    primes = prime_factors(int(input_integer))
    print(" * ".join(map(str, primes)), "=", input_integer)
else:
    print("The input is not an integer.")
