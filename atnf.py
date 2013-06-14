import browse_extract as b
import erocat, datetime
from numpy import *

res = b.heasarc('atnfpulsar','Crab',1e8,fields='name,period,period_dot,corr_age,ra,dec,ra_error,dec_error,lii,bii,pulsar_type,e_dot,distance',max_results=100000)

def flux(p,pdot,tauc,d):
    """docstring for logl"""
    if tauc<=1.7e4:
        a,b,c=63.9,-5.23,2.84
    else:
        a,b,c=39.27,-3.18,0.77
    return 10**(a+b*log10(p)+c*log10(pdot))/(4*pi*(d*3e21)**2)


# cln = {u'RADIO PULSAR':1800, u'STAR':2900, u'X-RAY PULSATOR':1810, u'ANOMALOUS X-RAY PULSAR':1840}
cln = {u'AXP,HE':1840, u'R':1800, u'AXP,NRAD':1840, u'NRAD':1800, u'HE':1810}
ef = [flux(*x) for x in zip(res.period[1],res.period_dot[1],res.corr_age[1],res.distance[1])]
cl = [cln[x] for x in res.pulsar_type[1]]
pos_err=sqrt(res.ra_error[1]**2+res.dec_error[1]**2)

table = erocat.mktable(nrows=len(pos_err))

table.data.field('IAUNAM')[:]=res.name[1]
table.data.field('ra')[:]=res.ra[1]
table.data.field('dec')[:]=res.dec[1]
table.data.field('lii')[:]=res.lii[1]
table.data.field('bii')[:]=res.bii[1]
table.data.field('radec_err')[:]=pos_err
table.data.field('poserr')[:]=pos_err
table.data.field('tb_flux')[:]=ef
table.data.field('class')[:]=cl
table.name = 'ero-src-list'
table.header.add_comment("Fluxes are estimated according to Vink et al, 2011 (http://adsabs.harvard.edu/abs/2011ApJ...727..131V) based on inputs from ATNF")
table.header.add_history('Initial version, V. Doroshenko, IAAT, %s'%datetime.date.isoformat(datetime.date.today()))
table.writeto('atnf.fits')


