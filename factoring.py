import math
import time
import csv
import random as rand

def trial_division(n, bound=-1):
    print("Trial Division")
    print("----factoring", n, "-------")
    a = []
    if bound == -1:
        bound = math.sqrt(n)

    #find all factors of 2
    while n % 2 == 0:
        a.append(2)
        n /= 2

    #find all odd factors
    f = 3
    while f <= bound:
        if n % f == 0:
            a.append(f)
            n /= f
        else:
            f += 2
    if n != 1: a.append(n)
    # Only odd number is possible
    return a

def fermat_factoring(n, M, verbose=False, trial_div=False):
    factors = []
    a = math.floor(pow(n, 1/2)) + 1
    i = 1
    x = 1
    u = pow(a, 2)
    print("Fermat_Factoring")
    print("----factoring", n, "-------")

    if n%2 == 0:
        return [2, n/2]

    while i <= M:  
 
        b = math.floor(pow(u-n, 1/2))
        # if verbose:
        #     print("===")
        #     print("i:", i)
        #     print("x:", x)
        #     print("a:", a)
        #     print("b:", b)
        #     print("b^2:", pow(b, 2))
        #     print("u:", u)
        #     print("u-n:", u-n)
        #     print("a+b:", a+b)
        #     print("a-b:", a-b)
        #     x += 1
        #if u-n is a square, u-n=b^2 and n = (a-b)(a+b)
        if pow(b, 2) == (u-n):
            factors.append(a-b)
            factors.append(a+b)
            return factors
        else:
            a = a + 1
            u = pow(a, 2)
            i = i + 1
    if trial_div:
        a = a - 1
        u = u + (2*a) + 1
        b = math.floor(pow(u-n, 1/2))
        # print("Trial Division with a-b:", a-b)
        return trial_division(n, a-b)
    return False

def fermat_factoring_sieve(n, M, verbose=False, trial_div=False):
    print("Fermat_Factoring Sieve")
    print("----factoring", n, "-------")
    factors = []
    a = math.floor(pow(n, 1/2)) + 1
    i = 1
    x = 1

    m = 20
    squares = {0:0, 1:1, 4:2, 5:3, 9:4, 16:5}
    map_of_sqrts = [[0, 10], [1, 9, 11, 19], [2, 8, 12, 18], [5, 15], [3, 7, 13, 17], [4, 6, 14, 16]]
    n_modded = n % m

    possible_asquare = [(x+n_modded)%m for x in squares]
    
    a_sqrts = []
    for i in possible_asquare:
        if i in squares:
            key = squares.pop(i)
            a_sqrts.extend(map_of_sqrts[key])

    while (a % m) not in a_sqrts:
        a = a+1
    u = pow(a, 2)


    if n%2 == 0:
        return [2, n/2]

    while i <= M:  
 
        b = math.floor(pow(u-n, 1/2))
        # if verbose:
        #     print("===")
        #     print("i:", i)
        #     print("x:", x)
        #     print("a:", a)
        #     print("b:", b)
        #     print("b^2:", pow(b, 2))
        #     print("u:", u)
        #     print("u-n:", u-n)
        #     print("a+b:", a+b)
        #     print("a-b:", a-b)
        #     x += 1
        #if u-n is a square, u-n=b^2 and n = (a-b)(a+b)
        if pow(b, 2) == (u-n):
            factors.append(a-b)
            factors.append(a+b)
            return factors
        else:
            a = a+1
            while (a % m) not in a_sqrts:
                a = a+1
            u = pow(a, 2)
            i = i + 1
    if trial_div:
        a = a - 1
        u = u + (2*a) + 1
        b = math.floor(pow(u-n, 1/2))
        # print("Trial Division with a-b:", a-b)
        return trial_division(n, a-b)
    return False

def pollard_rho(n, s_val=2):
    print("Pollard Rho")
    print("----factoring", n, "-------")
    x = y = s_val
    d = 1

    if n%2 == 0:
        return [2, n/2]

    while d == 1:
        x = g_func(x, n)
        y = g_func(g_func(y, n), n)
        d = math.gcd(abs(x-y), n)
    
    if d == n:
        return False
    else:
        return d
        
def g_func(x, n):
    return (pow(x, 2)+1)%n

###Factoring Interesting Numbers
#primes = [ 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199]
 
filename = 'fermat_nums.csv'
with open(filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['k', 'n', 'TD Time', 'TD Result', 'FF Time', 'FF Result', 'FFTD Time', 'FFTD Result','SFF Time', 'SFF Result','SFFTD Time', 'SFFTD Result', 'PR Time', 'PR Result', 'PR Trials', 'PR Final X'])
    for i in primes:
        print(i)
        num = pow(2, pow(2, i)) +1
        td_start = time.time()
        td_result = trial_division(num)
        td_end = time.time()

        ff_start = time.time()
        ff_result = fermat_factoring(num, max(20, num/2))
        ff_end = time.time()

        fftd_start = time.time()
        fftd_result = fermat_factoring(num,  999999, trial_div=True)
        fftd_end = time.time()

        sff_start = time.time()
        sff_result = fermat_factoring_sieve(num, max(20, num/2))
        sff_end = time.time()

        sfftd_start = time.time()
        sfftd_result = fermat_factoring_sieve(num,  999999, trial_div=True)
        sfftd_end = time.time()

        
        rand_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        x = rand_list.pop(rand.randint(0, len(rand_list)-1))

        pr_start = time.time()
        pr_result = pollard_rho(num, x)
        if ff_result[0] != 1:
            while pr_result == False & len(rand_list) > 0:
                print("len rand_list", len(rand_list))
                x = rand_list.pop(rand.randint(0, len(rand_list)-1))
                pr_result = pollard_rho(num, x)
        pr_end = time.time()
        trials = 9 - len(rand_list)


        writer.writerow([i, num, td_end-td_start, td_result, ff_end-ff_start, ff_result, fftd_end-fftd_start, fftd_result, sff_end-sff_start, sff_result, sfftd_end-sfftd_start, sfftd_result, pr_end-pr_start, pr_result, trials, x])

