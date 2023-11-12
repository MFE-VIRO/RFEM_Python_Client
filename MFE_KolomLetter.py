def Kolomletter(KolomGetal: int=1):
    if int(KolomGetal/26.00001)>0:
        Letter=chr(int(KolomGetal/26.00001)+64) + chr(KolomGetal-26*int(KolomGetal/26.00001)+64)
    else:
        Letter=chr(KolomGetal+64)
    return Letter

#TODO: Functie ook geschikt maken voor de situatie waarin 3 of meer letters nodig zijn...