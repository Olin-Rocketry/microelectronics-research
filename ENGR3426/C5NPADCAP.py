#------------------------------------------------------------------------------
#
# C5N pad capacitor Pcell for extraction
#
#------------------------------------------------------------------------------

# Import the db wrappers.
from ui import *
from math import *

def C5NPADCAP(cv, ptlist=[[0,0],[2100,0],[2100,2100],[0,2100]]):
    lib = cv.lib()
    dbu = float(lib.dbuPerUU())
    npts = len(ptlist)

    # Area capacitance in F/um^2.
    areacap = 0.027e-15
    # Perimeter capacitance in F/um.
    pericap = 0.

    # Compute the capacitor area and perimeter, assuming the capacitor is
    # a rectilinear shape.
    asum = 0.0
    perimeter = 0.0
    i = npts-1
    j = 0
    while j<npts:
        dx = float(ptlist[i][0])/dbu
        dy = float(ptlist[i][1])/dbu
        dx1 = float(ptlist[j][0])/dbu
        dy1 = float(ptlist[j][1])/dbu
        perimeter = perimeter + sqrt((dx1 - dx)**2 + (dy1 - dy)**2)
        asum = asum + (dx + dx1)*(dy1 - dy)
        i = j
        j = j + 1

    # The actual area is half the sum.
    area = 0.5*asum

    # Compute the capacitance.
    cap = areacap*area + pericap*perimeter

    # Update the master pcell property.
    cv.dbAddProp('c', cap)

    # Create the recognition region shape.
    xpts = intarray(npts)
    ypts = intarray(npts)
    for i in range(npts):
        xpts[i] = ptlist[i][0]
        ypts[i] = ptlist[i][1]
    cv.dbCreatePolygon(xpts, ypts, npts, TECH_Y0_LAYER);

    # Create pins.
    top_net = cv.dbCreateNet('G')
    cv.dbCreatePin('G', top_net, DB_PIN_INPUT)
    bot_net = cv.dbCreateNet('S')
    cv.dbCreatePin('S', bot_net, DB_PIN_INPUT)

    # Update the bounding box.
    cv.update()
