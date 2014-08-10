If you have two fractions, you can add them like this:

    import fractions
    fractions.Fraction("1/4") + fractions.Fraction("-6/25")
    # gives
    # Fraction(1, 100)
This library does the opposite:

    import break_fract
    break_fract.break_fract(7234823, 92374893)
    # gives
    # [Fraction(-1, 9), Fraction(2, 169), Fraction(10786, 60733)]

That's it, really.

Oh, and it's GPL licensed. I'll license it under something else if you
ask me to.
