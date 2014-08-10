#!/usr/bin/python
# Written by Nick O'Dell
# GPL

import fractions
from fractions import Fraction

def gcd(*inp):
    """Ignore zeros, and accept however many arguments"""
    try:
        return reduce(fractions.gcd, filter(lambda x: x != 0, inp))
    except:
        # No non-zero elements
        return None


def _isolve(a, b, c):
    """Solves a three-term diophantine eqn, of the form ax + by = c
    where all variables are integers
    Params: a, b, c
    Returns: x, y"""
    assert type(a) in [type(int()), type(long())]
    assert type(b) in [type(int()), type(long())]
    assert type(c) in [type(int()), type(long())]
    def _isolve_inner(a, b, c):
        # Quickly return if 0, 0 would work.
        if c == 0:
            return (0, 0)
        # Quickly return if a or b is factor of c.
        # Might cause a div-by-zero error.
        try:
            if c % a == 0:
                return (c/a, 0)
            elif c % b == 0:
                return (0, c/b)
        except: pass
        # Tests if the gcd of a and b is a factor of c.
        # If not, this equation is unsolvable.
        g = gcd(a, b)
        if g != None and c % g == 0:
            q, r = divmod(a, b)
            u, v = _isolve_inner(b, r, c)
            return (v, u - q*v)
        else:
            raise Exception("No solution to diophantine eqn %sx + %sy = %s." % (a, b, c))
    x, y = _isolve_inner(a, b, c)
    assert type(x) in [type(int()), type(long())]
    assert type(y) in [type(int()), type(long())]
    assert a*x + b*y == c
    return x, y


def _get_smallest_factor(num):
    """Returns: (smallest factor, remaining factors)
    Or false, if num is prime/square"""
    n = 2
    while True:
        if n*n >= num:
            return False
        if num % n == 0:
            # Found a factor. Check if there are other factors of the same size.
            n2 = n
            while True:
                if num % (n2 * n) == 0:
                    n2 *= n
                else:
                    if num / n2 == 1:
                        return False
                    return (n2, num / n2)
        n += 1


def _optimize(fraction_list):
    """In-place"""
    whole_number = 0
    for i, fraction in enumerate(fraction_list):
        q, r = divmod(fraction.numerator, fraction.denominator)
        whole_number += q
        fraction_list[i] = Fraction(r, fraction.denominator)
    # Re-add the whole number to the fraction with the smallest denominator
    def _temp(f1, f2):
        return f1 if f1[1].denominator < f2[1].denominator else f2
    i, smallest = reduce(_temp, enumerate(fraction_list))
    fraction_list[i] = Fraction(smallest.numerator + whole_number * smallest.denominator, smallest.denominator)

def break_fract(*inp):
    if type(inp[0]) == type(Fraction):
        inp = inp[0]
    else:
        inp = Fraction(*inp)

    ret = _get_smallest_factor(inp.denominator)
    if ret == False:
        if inp != 0:
            return [inp]
        else:
            return []
    else:
        denom1, denom2 = ret
        num2, num1 = _isolve(denom1, denom2, inp.numerator)
        f1 = Fraction(num1, denom1)
        f2 = Fraction(num2, denom2)
        fraction_list = break_fract(f2)
        fraction_list = [f1] + fraction_list
        _optimize(fraction_list)
        assert sum(fraction_list) == inp
        return fraction_list

        

if __name__ == "__main__":
    inp = Fraction("7234823/92374893")
    print(break_fract(inp))

