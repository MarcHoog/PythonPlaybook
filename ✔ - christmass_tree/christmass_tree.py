def holidaybush2_0(n):
    if n < 5:
        n = 5
    for i in range(n):
        print(("+" * (i * 2 + 1)).center(n * 2 - 1))

    print('| |'.center(n * 2))
    print('\=======/'.center(n * 2))


if __name__ == '__main__':
    holidaybush2_0(10)
