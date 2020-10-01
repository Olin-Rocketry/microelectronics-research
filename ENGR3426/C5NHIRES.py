#------------------------------------------------------------------------------
#
# C5N hires resistor Pcell for extraction
#
#------------------------------------------------------------------------------

from ui import *
from math import *

def C5NHIRES(cv, ptlist=[[0,0],[1000,0],[1000,1000],[0,1000]], l=1.0, w=1.0, nsquares=1.0, nbends=0) :
    lib = cv.lib()
    dbu = float(lib.dbuPerUU())
    npts = len(ptlist)

    # Sheet resistance for this resistor in ohms/square.
    rsh = 1023.
    # Number of squares a bend adds.
    bendFactor = 0.56

    length = l * dbu
    width =  w * dbu
    numBends = nbends

    # Now compute r.
    r = rsh * ((length / width) + (numBends * bendFactor))

    # Update the master pcell property.
    cv.dbAddProp("r", r)

    # Create the recognition region shape.
    xpts = intarray(npts)
    ypts = intarray(npts)
    for i in range (npts) :
        xpts[i] = ptlist[i][0]
        ypts[i] = ptlist[i][1]

    cv.dbCreatePolygon(xpts, ypts, npts, TECH_Y0_LAYER)

    # Create pins.
    plus_net = cv.dbCreateNet("A")
    cv.dbCreatePin("A", plus_net, DB_PIN_INPUT)
    minus_net = cv.dbCreateNet("B")
    cv.dbCreatePin("B", minus_net, DB_PIN_INPUT)

    # Update the bounding box.
    cv.update()
