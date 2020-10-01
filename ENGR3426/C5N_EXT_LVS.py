#------------------------------------------------------------------------------
#
# C5N extraction script
#
#------------------------------------------------------------------------------

from ui import *
ui = cvar.uiptr
cv = ui.getEditCellView()
geomBegin(cv)
lib = cv.lib()

print 'Loading pcells for extraction...'
ui.loadPCell(lib.libName(), 'C5NNMOS')
ui.loadPCell(lib.libName(), 'C5NPMOS')
ui.loadPCell(lib.libName(), 'C5NP1RES')
ui.loadPCell(lib.libName(), 'C5NP2RES')
ui.loadPCell(lib.libName(), 'C5NHIRES')
ui.loadPCell(lib.libName(), 'C5NP1P2CAP')
ui.loadPCell(lib.libName(), 'C5NPADCAP')

print 'Getting raw layers...'
nwell = geomGetShapes('nwell', 'drawing')
active = geomGetShapes('active', 'drawing')
poly = geomGetShapes('poly', 'drawing')
nselect = geomGetShapes('nselect', 'drawing')
pselect = geomGetShapes('pselect', 'drawing')
poly2 = geomGetShapes('poly2', 'drawing')
hires = geomGetShapes('hires', 'drawing')
contact = geomGetShapes('contact', 'drawing')
polycontact = geomGetShapes('polycontact', 'drawing')
activecontact = geomGetShapes('activecontact', 'drawing')
poly2contact = geomGetShapes('poly2contact', 'drawing')
metal1 = geomGetShapes('metal1', 'drawing')
via = geomGetShapes('via', 'drawing')
metal2 = geomGetShapes('metal2', 'drawing')
via2 = geomGetShapes('via2', 'drawing')
metal3 = geomGetShapes('metal3', 'drawing')
glass = geomGetShapes('glass', 'drawing')
pads = geomGetShapes('pads', 'drawing')
cap_id = geomGetShapes('cap_id', 'drawing')
res_id = geomGetShapes('res_id', 'drawing')
diode_id = geomGetShapes('diode_id', 'drawing')

print 'Forming derived layers...'
bkgnd = geomBkgnd()
psub = geomAndNot(bkgnd, nwell)
gate = geomAnd(poly, active)
ngate = geomAnd(gate, nselect)
pgate = geomAnd(gate, pselect)
diff = geomAndNot(active, gate)
ndiff = geomAnd(diff, nselect)
pdiff = geomAnd(diff, pselect)
nplug = geomAnd(ndiff, nwell)
pplug = geomAndNot(pdiff, nwell)
activecon = geomOr(geomAnd(contact, active), activecontact)
polycon = geomOr(geomAnd(contact, poly), polycontact)
poly2con = geomOr(geomAnd(contact, poly2), poly2contact)
poly_wire = geomAndNot(poly, res_id)
poly_res = geomAnd(poly, res_id)
poly2_wire = geomAndNot(poly2, geomOr(res_id, hires))
poly2_res = geomAnd(poly2, res_id)
poly2_hires = geomAnd(poly2, hires)
p1p2_cap = geomAnd(poly, geomAnd(poly2, cap_id))
pad_cap = geomAnd(metal1, pads)

print 'Labeling nodes...'
geomLabel(poly_wire, 'poly', 'pin', True)
geomLabel(poly2_wire, 'poly2', 'pin', True)
geomLabel(metal1, 'metal1', 'pin', True)
geomLabel(metal2, 'metal2', 'pin', True)
geomLabel(metal3, 'metal3', 'pin', True)
geomLabel(poly_wire, 'poly', 'net', False)
geomLabel(poly2_wire, 'poly2', 'net', False)
geomLabel(metal1, 'metal1', 'net', False)
geomLabel(metal2, 'metal2', 'net', False)
geomLabel(metal3, 'metal3', 'net', False)

print 'Forming connectivity...'
geomConnect([[pplug, psub, pdiff], 
             [nplug, nwell, ndiff], 
             [activecon, ndiff, pdiff, metal1], 
             [polycon, poly_wire, metal1], 
             [poly2con, poly2_wire, metal1], 
             [via, metal1, metal2], 
             [via2, metal2, metal3]])

# Save connectivity to extracted view. Saved layers must be
# ones previously connected by geomConnect. Any derived
# layers must be saved to a named layer (e.g. psub below)
print 'Saving interconnect...'
saveInterconnect([[psub, 'psub'], 
                  nwell, 
                  [ndiff, 'active'], 
                  [pdiff, 'active'],
                  [nplug, 'active'], 
                  [pplug, 'active'],
                  [poly_wire, 'poly'], 
                  [poly2_wire, 'poly2'], 
                  [activecon, 'activecontact'], 
                  [polycon, 'polycontact'], 
                  [poly2con, 'poly2contact'], 
                  metal1, 
                  via, 
                  metal2, 
                  via2, 
                  metal3])

# Extract MOS devices. Device terminal layers *must* exist in
# the extracted view as a result of saveInterconnect.
# In this case we are using pcell devices which will be
# created according to the recognition region polygon.
print 'Extracting MOS devices...'
extractMOS('C5NNMOS', ngate, poly, active, psub)
extractMOS('C5NPMOS', pgate, poly, active, nwell)

# Extract resistors. Device terminal layers must exist in
# extracted view as a result of saveInterconnect.
if geomNumShapes(poly_res)>0:
    print 'Extracting poly1 resistors...'
    extractRes('C5NP1RES', poly_res, poly_wire)
if geomNumShapes(poly2_res)>0:
    print 'Extracting poly2 resistors...'
    extractRes('C5NP2RES', poly2_res, poly2_wire)
if geomNumShapes(poly2_hires)>0:
    print 'Extracting hires resistors...'
    extractRes('C5NHIRES', poly2_hires, poly2_wire)

# Extract poly1-poly2 capacitors. Device terminal layers must exist in
# extracted view as a result of saveInterconnect.
if geomNumShapes(p1p2_cap)>0:
    print 'Extracting poly1-poly2 capacitors...'
    extractMosCap('C5NP1P2CAP', p1p2_cap, poly2, poly)

# Extract pad capacitors. Device terminal layers must exist in 
# extracted view as a result of saveInterconnect.
if geomNumShapes(pad_cap)>0:
    print 'Extracting pad capacitors...'
    extractMosCap('C5NPADCAP', pad_cap, metal1, psub)

# Exit geometry package, freeing memory.
print 'Extraction completed.'
geomEnd()

# Open the extracted view.
ui.openCellView(lib.libName(), cv.cellName(), 'extracted')
