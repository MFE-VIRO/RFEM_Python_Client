def interpol(x=1.0,x1 = 0.0, x2=2.0,y1=5.0,y2=10.0):
    y = y1 + (x - x1) / (x2 - x1) * (y2 - y1)
    return y

def left(s, amount):
    return s[:amount]

def right(s, amount):
    return s[-amount:]

def KolomLetter(KolomGetal: int=1):
    if int(KolomGetal/26.00001)>0:
        Letter=chr(int(KolomGetal/26.00001)+64) + chr(KolomGetal-26*int(KolomGetal/26.00001)+64)
    else:
        Letter=chr(KolomGetal+64)
    return Letter

    #TODO: Functie ook geschikt maken voor de situatie waarin 3 of meer letters nodig zijn...