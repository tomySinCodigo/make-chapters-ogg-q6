def getNRows(n:int, cols:int=3) -> list:
    return [(irow, icol) \
        for irow, _ in enumerate(range(0,n,cols)) \
        for icol in range(cols)]

if __name__ == '__main__':
    res = getNRows(19)
    print(f'numeros de filas: {res[-1][0]}')
    print(res)