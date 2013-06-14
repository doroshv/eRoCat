import browse_extract as b
import erocat, datetime
from numpy import *

res = b.heasarc('hmxbcat','Crab',1e8,max_results=1000,fields='name,ra,dec,lii,bii,fx,class')


cln={u'HMXRB X-RAY PULSAR':1110,
     u'HMXRB BE STAR ECLIPSING':1313,
     u'HMXRB':1100,
     u'HMXRB SUPERGIANT X-RAY PULSAR':1210,
     u'HMXRB SUPERGIANT':1200,
     u'HMXRB BE STAR X-RAY PULSAR':1310,
     u'HMXRB BE STAR':1300,
     u'HMXRB SUPERGIANT X-RAY PULSAR ECLIPSING':1213,
     u'HMXRB X-RAY PULSAR ECLIPSING':1113,
     u'HMXRB SUPERGIANT ECLIPSING':1203}

cl = [cln[x] for x in res.class_name[1]]


table = erocat.mktable(nrows=len(res.ra[1]))

table.data.field('IAUNAM')[:]=res.name[1]
table.data.field('ra')[:]=res.ra[1]
table.data.field('dec')[:]=res.dec[1]
table.data.field('lii')[:]=res.lii[1]
table.data.field('bii')[:]=res.bii[1]
table.data.field('radec_err')[:]=ones_like(res.ra[1])*0.1
table.data.field('poserr')[:]=ones_like(res.ra[1])*0.1
table.data.field('tb_flux')[:]=res.fx[1]*2.4e-12
table.data.field('class')[:]=cl
table.name = 'ero-src-list'
table.header.add_comment("converted from Catalogue of high-mass X-ray binaries in the Galaxy (4th edition) (2006A&A...455.1165L)")
table.header.add_history('Initial version, V. Doroshenko, IAAT, %s'%datetime.date.isoformat(datetime.date.today()))
table.writeto('hmxbcat.fits')


