#!/usr/bin/python
# Written by Nick O'Dell
# GPL

import fractions
from fractions import Fraction
import miller_rabin

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


def _smallest_factor(num, check_to=10000):
    n = 2
    while n < 10000 and n*n < num:
        if num % n == 0:
            return n
        n += 1
    raise Exception("Couldn't find factor")

def _get_smallest_factor_and_other_factors_of_same_size(num):
    """Returns: (smallest factor, remaining factors)
    Or false, if num is prime/square"""
    if miller_rabin.probablyPrime(num, 100):
        return False
    # Found a factor. Check if there are other factors of the same size.
    try:
        n = _smallest_factor(num)
        n2 = n
        while True:
            if num % (n2 * n) == 0:
                n2 *= n
            else:
                return (n2, num / n2)
            if num / n2 == 1:
                # All that's left is a square/cube
                return False
    except:
        return False


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

    ret = _get_smallest_factor_and_other_factors_of_same_size(inp.denominator)
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
    inp = Fraction("2846525407272135136458680072628476464590145139160552871880638155009214845791027012368044072260703427803287822396645791272857443850333605515345564361626979025164851622070484228657707972206869894375689896643273027861256544474577406123302271693725031709168133139791511099709113085589560823052113521695703565073410984968270463985021693127625984196966606788447651345617651128861913813851572785993894162831527428040369133782843031449327554955005310198062703862254362084561068622072910226747418147436796264104037826128444308313818885844632568824791659481087842623483461895444306576712154513956760783537533022864630841701839507381326593848177550073324037776436322863157851653429560679303224859734988618844068870297948449550659954680621891331857017096393396734999351560098317304418326953024243629891095501537925107754543523205908437115746048484767730054341933759579511693488360791190945393447455086519753559130140171731964148589051258181113214208951735061848142933803910862568037832263277153184306062685068651/7807362367922261933218564234091175596677006073236340010681752556738275954274188306189677768834391445789688003364699235357044228867283659317547494817191578220646254443354879028041296065951480157196159748431357252860854145550678953748334537620448284406544570787516611480101629661326870126228716757192857479665383831698284123866899554382851633108798270320574811834579830930437481156937989417806470584218511988088665834741876495955958763794001853413150831895460841624736391456376965545809172617280634665506234224019790365222419203185728472591457216268874905807600873161073288895507298647782406517223643953573587392408559701132267060198088221824029893619300321994052173290251717055664168204184362040347518827510001706593214389108615338968446290473199691934174300160987822232078895147173416409342368381324038978690240622935546937844929722126927309880851124412238471938655869455632897635260286062807919819543089336286429011040866635101948377576468245788955082466266872218688320985598225503303685100834818579")
    print(break_fract(inp))

