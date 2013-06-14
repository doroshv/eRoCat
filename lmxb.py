import browse_extract as b
import erocat, datetime, pyfits
from numpy import *

res = b.heasarc('lmxbcat','Crab',1e8,max_results=1000,fields='name,ra,dec,lii,bii,flux,xray_type')

# for q in res.name[1]:
#     res1=b.heasarc('RITTERLMXB',res.name[1][0],1,max_results=10,fields='name,ra,dec,acc_pos,lii,bii,type1,class',convert_fields=False)



# rar = array(res1.ra[1],dtype=float32)
# der = array(res1.dec[1],dtype=float32)

ra,dec,pose,clas,lii,bii = [],[],[],[],[],[]
for i in range(len(res.name[1])):
    print i, len(res.name[1])
    res1=b.heasarc('RITTERLMXB',"%s,%s"%(res.ra[1][i],res.dec[1][i]),30.,max_results=10,fields='name,ra,dec,acc_pos,lii,bii,type1',convert_fields=False)
    try:
        print res1.name[1],res1.Search_Offset[1]
        if len(res1.name[1])==1:
            f = True
        else:
            f = False
    except:
        f = False
    if f:
        ra.append(float(res1.ra[1][0]))
        dec.append(float(res1.dec[1][0]))
        pose.append(float(res1.acc_pos[1][0]))
        lii.append(float(res1.lii[1][0]))
        bii.append(float(res1.bii[1][0]))
    else:
        ra.append(res.ra[1][i])
        dec.append(res.dec[1][i])
        lii.append(res.lii[1][i])
        bii.append(res.bii[1][i])
        pose.append(30.)

       
    
    
    
    
# parse class

pc = lambda x:1400+x.count('P')*10+x.count('B')*80+max(x.count('E')*3,x.count('T')*5)
cl = [pc(x) for x in res.xray_type[1]]
# adist=lambda ra1,d1,ra2,d2: arccos(sin(d1)sin(d2) + cos(d1)cos(d2)cos(ra1 - ra2))
# f='lmxbxcor.fits'
# ra = list(pyfits.getdata(f).field('a_ra'))
# dec = list(pyfits.getdata(f).field('a_dec'))
# pose = list(pyfits.getdata(f).field('a_acc_pos'))

# s1 = set([str(x) for x in res.name[1]])
# s2 = set(pyfits.getdata(f).field('b_name'))
# missing = s1.difference(s2)


table = erocat.mktable(nrows=len(res.ra[1]))

table.data.field('IAUNAM')[:]=res.name[1]
table.data.field('ra')[:]=ra
table.data.field('dec')[:]=dec
table.data.field('lii')[:]=lii
table.data.field('bii')[:]=bii
table.data.field('radec_err')[:]=pose
table.data.field('poserr')[:]=pose
table.data.field('tb_flux')[:]=res.flux[1]*2.4e-12
table.data.field('class')[:]=cl
table.name = 'ero-src-list'
table.header.add_comment(
"""based on Fourth Edition of the Catalog of Low-mass X-ray Binaries (LMXBs) and (2007A&A...469..807L) and Catalog of Cataclysmic Binaries, Low-Mass X-ray Binaries, and Related Objects (7th Edition, rev. 7.17, May 2012) of Ritter & Kolb. The former has more sources but poor position uncertainty, so coordinates from Ritter&Kolb are used if possible. If 2 or more sources from Liu et al 2007 might be associated with one from Ritter&Kolb, all are taken from Liu et al 2007.""")
table.header.add_history('Initial version, V. Doroshenko, IAAT, %s'%datetime.date.isoformat(datetime.date.today()))
table.writeto('lmxbcat.fits')


