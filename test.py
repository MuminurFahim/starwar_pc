n = 395


def formula(a, b, c):
    return (a - b) / (c - b) * 100


def convert(z):
    return str(int(z))


def display(a, b, c, string):
    d = formula(a, b, c)
    e = convert(d)
    print(f'{e}% of {string}-2')


display(n, 266, 516, 'part')
display(n, 354, 426, 'project')

