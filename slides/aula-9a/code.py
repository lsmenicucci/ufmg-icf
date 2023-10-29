def intepolate_lagr(xb, yb, x):
    # a lista do valor do polinomios em x
    plist = yb.copy()
    order = 1
    
    # modificamos a lista passo a passo para que os polinomios incluam mais pontos
    # quando len(plist) = 1 é porque chegamos no polinomio de ordem n (o final da arvore)
    while len(plist) > 1:
        # a nova lista que substituira a antiga
        new_plist = []
        
        # jutamos o polinomio i com o i+1
        for i in range(len(plist) - 1):
            p = (x - xb[order + i]) * plist[i] + (xb[i] - x) * plist[i + 1]
            p /= (xb[i] - xb[i + order])

            new_plist.append(p) 

        plist = new_plist
        order += 1

    return plist[0]
    
# provide test data with different order
test_data = [
    ([0, 1, 2], [0, 1, 4], 0.5),
    ([-4, -2, 0, 2, 4], [16, 4, 0, 4, 16], 1),
    ([-9.4, 12, 0.4], [0.002, 0.004, 0.006], 0.5),
    ([0, 1, 2, 3], [0, 1, 4, 9], 0.5),
]

from scipy.interpolate import lagrange

for test_x, test_y, x in test_data:
    my = intepolate_lagr(test_x, test_y, x)
    lib = lagrange(test_x, test_y)(x)

    print(f"my: {my:12.6f}, lib: {lib:12.6f}, diff: {abs(my - lib):12.6f}")
