#------------------------------------------------------------------------------
#
# C5N nmos Pcell for extraction
#
#------------------------------------------------------------------------------

from ui import *

def C5NNMOS(cv, ptlist=[[0,0],[1800,0],[1800,1800],[0,1800]]) :
    lib = cv.lib()
    dbu = lib.dbuPerUU()

    # Create the recognition region shape.
    npts = len(ptlist)
    xpts = intarray(npts)
    ypts = intarray(npts)
    for i in range (npts) :
        xpts[i] = ptlist[i][0]
        ypts[i] = ptlist[i][1]
    cv.dbCreatePolygon(xpts, ypts, npts, TECH_Y0_LAYER);

    # Create pins.
    gate_net = cv.dbCreateNet('G')
    cv.dbCreatePin('G', gate_net, DB_PIN_INPUT)
    source_net = cv.dbCreateNet('S')
    cv.dbCreatePin('S', source_net, DB_PIN_INPUT)
    drain_net = cv.dbCreateNet('D')
    cv.dbCreatePin('D', drain_net, DB_PIN_INPUT)
    bulk_net = cv.dbCreateNet('B')
    cv.dbCreatePin('B', bulk_net, DB_PIN_INPUT)

    # Update the bounding box.
    cv.update()
