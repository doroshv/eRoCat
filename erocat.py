import pyfits,re

"""
Author: Victor Doroshenko IAAT, Tuebingen, Germany (doroshv@astro.uni-tuebingen.de)
Feel free to ask questions or contribute to the project.
"""

da = open('cat_desc.txt','r').readlines()
n =3

def reformat(x,n=n):
    """docstring for reform_col"""
    if x.find('x')>0:
        x=x.replace('R','D').replace('n',str(n)).replace('*','')
        d = x.split('x')
        return "P%s(%s)"%(d[1],d[0])
    else:
        return x.replace('R','D')

def splitstr(x,n=n):
    """docstring for splitstr"""
    x = x.split()
    cn = x[0]
    cf = reformat(x[1],n)
    if x[2][0]=='[':
        cu=x[2][1:-1]
        cd = " ".join(x[3:])
        return cn,cf,cu,cd
    else:
        cu = ''
        cd = " ".join(x[2:])
        return cn,cf,cu,cd


coldesc = [splitstr(x) for x in da]

def mktable(cd=coldesc,nrows=0,fill=True):
    """docstring for mkfitsfile"""
    cols=[]
    for x in cd:
        cols.append(pyfits.Column(name=x[0],format=x[1],unit=x[2]))
    return pyfits.new_table(cols,nrows=nrows,fill=fill)



