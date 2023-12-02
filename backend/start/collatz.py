

def collatz(x):
    if x % 2 == 0:
        return x // 2
    else:
        return 3 * x + 1
    
def collatz_sequence(x):
    sequence = [x]
    while x != 1:
        x = collatz(x)
        sequence.append(x)
    return sequence


nums_seen = set()
for i in range(0, 5):
    x0 = 6*(6*i+1)+1 # y = 36*i+7
    y = 32*(6*i+1)+5 # y = 6*(32*i+6)+1
    z = 8*(32*i+6)+1
    seq = collatz_sequence(x0)
    print(z, y, f"\033[93m{x0}\033[0m", [s for s in seq[1:30] if s % 2 == 1])

    
