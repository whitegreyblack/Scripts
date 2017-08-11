# calc.py
symbol = {'+','-','*','/','**'}

def evaluate(x, reg):
    try:
        if 'x' is x:
            return reg
        elif 'x' in x and reg is not None:
            x = x.replace('x','{}'.format(reg))
        elif x[0] in symbol:
            x = '{}'.format(reg)+x
        return eval(x)
    except:
        print('Error')
        return 0

def main(x=0):
    print('[Python Expression Calculator]')
    while 1:
        x = evaluate(input('>>> x = ').replace(" ", ""), x)
        print('... {}'.format(x) if x is not None else '...') 


if __name__ == "__main__":
    main()
