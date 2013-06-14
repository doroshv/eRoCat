from numpy import *
import commands, datetime
import erocat
from astropysics.coords import FK5Coordinates,GalacticCoordinates

data = open('ulx/table.tex','r').readlines()

ra = [x.split('&')[0].strip() for x in data]
dec = [x.split('&')[1].strip() for x in data]
name = [x.split('&')[2].strip()+' X-'+x.split(r'\\')[-1].split()[-1] for x in data]
d = [float(x.split('&')[3].strip()) for x in data]
lx1 = [x.split('&')[8].strip() for x in data]
lx2 = [x.split('&')[9].strip() for x in data]
lx = []

tnh,flf=loadtxt('ulx/absfrac.txt')

for l in zip(lx1,lx2):
    try:
        l1=float(l[0])
    except:
        l1=nan
    try:
        l2=float(l[1])
    except:
        l2=nan
    lx.append(nanmin((l1,l2)))

def detnh(ra,dec):
    """docstring for detnh"""
    return float(commands.getstatusoutput('nh 2000 '+str(ra)+' '+str(dec))[-1].split()[-1])

def get_absflux(ra,dec,lx,d):
    """docstring for get_absflux"""
    flux = 1e39*lx/(4*pi*(3.085e24*d)**2)
    nh = detnh(ra,dec)/1e22
    flux*=flf[tnh.searchsorted(nh)]
    return flux

flux = [get_absflux(*x) for x in zip(ra,dec,lx,d)]

deg = lambda ra,dec:(FK5Coordinates(ra,dec).ra.degrees,FK5Coordinates(ra,dec).dec.degrees)
gdeg = lambda ra,dec:(FK5Coordinates(ra,dec).convert(GalacticCoordinates).long.degrees,FK5Coordinates(ra,dec).convert(GalacticCoordinates).lat.degrees)

radeg = [deg(*x)[0] for x in zip(ra,dec)]
decdeg = [deg(*x)[1] for x in zip(ra,dec)]
lii = [gdeg(*x)[0] for x in zip(ra,dec)]
bii = [gdeg(*x)[1] for x in zip(ra,dec)]

table = erocat.mktable(nrows=len(flux))

table.data.field('IAUNAM')[:]=name
table.data.field('ra')[:]=radeg
table.data.field('dec')[:]=decdeg

table.data.field('lii')[:]=lii
table.data.field('bii')[:]=bii
table.data.field('radec_err')[:]=ones_like(lii)*0.1
table.data.field('poserr')[:]=ones_like(lii)*0.1
table.data.field('tb_flux')[:]=flux
table.data.field('class')[:]=[9300]*len(flux)
table.name = 'ero-src-list'
table.header.add_comment("Based on Swartz et al 2001, (2011ApJ...741...49S). Of two estimates for Lx the smaller was used to convert the flux to absorbed value using galactic nH map (reversed the procedure used by Swartz et al)")
table.header.add_history('Initial version, V. Doroshenko, IAAT, %s'%datetime.date.isoformat(datetime.date.today()))
table.writeto('ulxcat.fits')

        

