def interpol(x=1.0,x1 = 0.0, x2=2.0,y1=5.0,y2=10.0):
    y = y1 + (x - x1) / (x2 - x1) * (y2 - y1)
    return y

def left(s, amount):
    return s[:amount]

def right(s, amount):
    return s[-amount:]
