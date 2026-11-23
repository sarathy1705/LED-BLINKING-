#!/usr/bin/env python3
"""Generate the NE555 LED blinker KiCad project using the installed KiCad 7 libraries."""
import os, re, uuid, csv, json, math
from pathlib import Path

ROOT = Path('/home/ubuntu/NE555_LED_Blinker')
ROOT.mkdir(parents=True, exist_ok=True)
PROJECT = 'NE555_LED_Blinker'

def uid(): return str(uuid.uuid4())

def extract_symbol(text, name):
    pat = re.compile(r'\(symbol\s+"' + re.escape(name) + r'"')
    m = pat.search(text)
    if not m: raise ValueError('Symbol not found: '+name)
    start=m.start(); depth=0; quoted=False; escaped=False
    for i in range(start,len(text)):
        c=text[i]
        if quoted:
            if escaped: escaped=False
            elif c=='\\': escaped=True
            elif c=='"': quoted=False
        else:
            if c=='"': quoted=True
            elif c=='(': depth+=1
            elif c==')':
                depth-=1
                if depth==0: return text[start:i+1]
    raise ValueError('Unclosed symbol '+name)

def symbol_def(lib, name):
    text=Path(f'/usr/share/kicad/symbols/{lib}.kicad_sym').read_text()
    s=extract_symbol(text,name)
    s=s.replace('(symbol "'+name+'"','(symbol "'+lib+':'+name+'"',1)
    return s

def get_pins(lib,name):
    s=extract_symbol(Path(f'/usr/share/kicad/symbols/{lib}.kicad_sym').read_text(),name)
    out=[]
    # Pin declarations are directly nested in unit sub-symbols. Extract each pin block.
    for m in re.finditer(r'\(pin\s+(?:input|output|bidirectional|tri_state|passive|power_in|power_out|open_collector|open_emitter|no_connect)\s+\w+\s+\(at\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\)',s):
        start=m.start(); d=0; q=False; esc=False
        for j in range(start,len(s)):
            c=s[j]
            if q:
                if esc: esc=False
                elif c=='\\': esc=True
                elif c=='"': q=False
            else:
                if c=='"': q=True
                elif c=='(': d+=1
                elif c==')':
                    d-=1
                    if d==0: block=s[start:j+1]; break
        num=re.search(r'\(number\s+"([^"]+)"',block)
        if num:
            out.append({'num':num.group(1),'x':float(m.group(1)),'y':float(m.group(2)),'angle':float(m.group(3))})
    # Shared/inherited pins are not a concern for these single-unit symbols; deduplicate by pin number.
    seen=set(); ded=[]
    for p in out:
        if p['num'] not in seen: ded.append(p); seen.add(p['num'])
    return ded

# All parts and exact official KiCad footprint assignments.
parts = [
 ('U1','Timer','NE555P','NE555P','Timer:NE555P','Package_DIP:DIP-8_W7.62mm','NE555 timer, PDIP-8'),
 ('R1','Device','R','1k','Device:R','Resistor_THT:R_Axial_DIN0309_L9.0mm_D3.2mm_P12.70mm_Horizontal','1 kOhm, 0.25 W or greater'),
 ('R2','Device','R','10k','Device:R','Resistor_THT:R_Axial_DIN0309_L9.0mm_D3.2mm_P12.70mm_Horizontal','10 kOhm, 0.25 W or greater'),
 ('R3','Device','R','220','Device:R','Resistor_THT:R_Axial_DIN0309_L9.0mm_D3.2mm_P12.70mm_Horizontal','220 Ohm, LED current limiting'),
 ('C1','Device','C_Polarized','100uF','Device:C_Polarized','Capacitor_THT:CP_Radial_D5.0mm_P2.00mm','100 uF electrolytic, >=10 V, radial 5 mm; pin 1 positive'),
 ('C2','Device','C','10nF','Device:C','Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm','10 nF ceramic control-pin capacitor'),
 ('C3','Device','C','100nF','Device:C','Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm','100 nF ceramic decoupling capacitor'),
 ('D1','Device','LED','LED_RED','Device:LED','LED_THT:LED_D5.0mm','Red LED, 5 mm'),
 ('J1','Connector_Generic','Conn_01x02','5V INPUT','Connector_Generic:Conn_01x02','TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2_1x02_P5.00mm_Horizontal','2-pin 5.00 mm terminal block; pin 1=+5V, pin 2=GND'),
]
# Schematic placement coordinates in mm; labels attach directly to actual library pin endpoints.
places={'U1':(150,90),'R1':(110,68),'R2':(110,103),'R3':(210,65),'C1':(195,120),'C2':(185,94),'C3':(110,137),'D1':(235,87),'J1':(85,92)}
# Every pin has one named net; these are also used to generate the PCB connectivity and BOM.
pinnets={
 'U1':{'1':'GND','2':'TIMING','3':'OUT','4':'+5V','5':'CTRL','6':'TIMING','7':'DISCH','8':'+5V'},
 'R1':{'1':'+5V','2':'DISCH'}, 'R2':{'1':'DISCH','2':'TIMING'},
 'R3':{'1':'OUT','2':'LED_A'}, 'C1':{'1':'TIMING','2':'GND'},
 'C2':{'1':'CTRL','2':'GND'}, 'C3':{'1':'+5V','2':'GND'},
 'D1':{'1':'GND','2':'LED_A'}, 'J1':{'1':'+5V','2':'GND'} }

# Embed library symbols verbatim so the schematic opens independently of global symbol-rescue state.
libids=[]
for ref,lib,name,val,libid,fp,desc in parts:
    if libid not in libids: libids.append(libid)
for libid in ['power:+5V','power:GND','power:PWR_FLAG']:
    if libid not in libids: libids.append(libid)
lib_defs=[]
for libid in libids:
    lib,name=libid.split(':',1)
    lib_defs.append(symbol_def(lib,name))

root_uuid=uid()
head=f'''(kicad_sch (version 20230121) (generator eeschema)
 (uuid {root_uuid})
 (paper "A4")
 (lib_symbols
'''+ '\n'.join(lib_defs)+'''\n )\n'''
body=[]
# component symbols
for ref,lib,name,val,libid,fp,desc in parts:
    x,y=places[ref]
    pins=get_pins(lib,name)
    body.append(f''' (symbol (lib_id "{libid}") (at {x:.4f} {y:.4f} 0) (unit 1)
  (in_bom yes) (on_board yes) (dnp no) (uuid {uid()})
  (property "Reference" "{ref}" (at {x:.4f} {y-8:.4f} 0) (effects (font (size 1.27 1.27))))
  (property "Value" "{val}" (at {x:.4f} {y-5.5:.4f} 0) (effects (font (size 1.27 1.27))))
  (property "Footprint" "{fp}" (at {x:.4f} {y:.4f} 0) (effects (font (size 1.27 1.27)) hide))
  (property "Datasheet" "" (at {x:.4f} {y:.4f} 0) (effects (font (size 1.27 1.27)) hide))
  {''.join(f'(pin "{p["num"]}" (uuid {uid()}))' for p in pins)}
  (instances (project "{PROJECT}" (path "/{root_uuid}" (reference "{ref}") (unit 1))))
 )''')
    # Name every electrical pin explicitly. This produces a readable, reliable netlist.
    for p in pins:
        num=p['num']
        if num not in pinnets.get(ref,{}): continue
        # KiCad schematic symbol local Y is positive upward; page Y increases downward.
        px=x+p['x']; py=y-p['y']; net=pinnets[ref][num]
        body.append(f''' (label "{net}" (at {px:.4f} {py:.4f} 0)
  (effects (font (size 1.0 1.0)) (justify left bottom)) (uuid {uid()}))''')
# Power symbols on input rail and ground; labels elsewhere connect these named nets globally.
def power_instance(libid, ref, value, at, root_uuid):
    x,y=at
    pins=get_pins('power',libid.split(':')[1])
    return f''' (symbol (lib_id "{libid}") (at {x:.4f} {y:.4f} 0) (unit 1)
  (in_bom yes) (on_board yes) (dnp no) (uuid {uid()})
  (property "Reference" "{ref}" (at {x:.4f} {y+2:.4f} 0) (effects (font (size 1 1)) hide))
  (property "Value" "{value}" (at {x:.4f} {y+3:.0f} 0) (effects (font (size 1 1))))
  (property "Footprint" "" (at {x:.4f} {y:.4f} 0) (effects (font (size 1 1)) hide))
  (property "Datasheet" "" (at {x:.4f} {y:.4f} 0) (effects (font (size 1 1)) hide))
  {''.join(f'(pin "{p["num"]}" (uuid {uid()}))' for p in pins)}
  (instances (project "{PROJECT}" (path "/{root_uuid}" (reference "{ref}") (unit 1))))
 )'''
# +5V power symbol at U1 pin 8; GND symbol at U1 pin 1; ERC flags on supply source rails.
body.append(power_instance('power:+5V','#PWR01','+5V',(150,79.84),root_uuid))
body.append(power_instance('power:GND','#PWR02','GND',(150,100.16),root_uuid))
body.append(power_instance('power:PWR_FLAG','#FLG01','PWR_FLAG',(79.92,92),root_uuid))
# ERC power flags identify the external 5 V input as the source for both rails.
body.append(power_instance('power:PWR_FLAG','#FLG02','PWR_FLAG',(150,100.16),root_uuid))
# A few visible notes on sheet.
# Add sheet title text.
body.append(f''' (text "NE555 ASTABLE LED BLINKER — 5 V" (at 150 42 0) (effects (font (size 2.0 2.0) (thickness 0.3)) (justify left bottom)) (uuid {uid()}))''')
body.append(f''' (text "Nominal: about 0.69 Hz; 0.76 s ON / 0.69 s OFF. C1 positive to TIMING." (at 150 48 0) (effects (font (size 1.2 1.2)) (justify left bottom)) (uuid {uid()}))''')
body.append(f''' (sheet_instances (path "/" (page "1")))\n)''')
(ROOT/f'{PROJECT}.kicad_sch').write_text(head+'\n'.join(body)+'\n')
# Native KiCad project settings template; the adjacent .kicad_sch and .kicad_pcb share this project name.
import shutil
shutil.copyfile('/usr/share/kicad/demos/custom_pads_test/custom_pads_test.kicad_pro', ROOT/f'{PROJECT}.kicad_pro')
# BOM and canonical pin-net list.
with (ROOT/'BOM.csv').open('w',newline='') as f:
    w=csv.writer(f); w.writerow(['Reference','Value','Description','Footprint','Quantity'])
    for ref,lib,name,val,libid,fp,desc in parts: w.writerow([ref,val,desc,fp,1])
with (ROOT/'connections.csv').open('w',newline='') as f:
    w=csv.writer(f); w.writerow(['Reference','Pin','Net'])
    for ref in pinnets:
        for pin,net in pinnets[ref].items(): w.writerow([ref,pin,net])
import pcbnew

def iu(mm): return pcbnew.FromMM(float(mm))
def vec(x,y): return pcbnew.VECTOR2I(iu(x),iu(y))

board=pcbnew.BOARD()
board.GetDesignSettings().SetBoardThickness(iu(1.6))
board.GetDesignSettings().m_TrackMinWidth=iu(0.25)
board.GetDesignSettings().m_ViasMinSize=iu(0.6)

netnames=['+5V','GND','TIMING','DISCH','OUT','LED_A','CTRL']
nets={}
for code,n in enumerate(netnames,1):
    net=pcbnew.NETINFO_ITEM(board,n); net.SetNetCode(code); board.Add(net); nets[n]=net

# Footprint placements are deliberately generous for first-time hand soldering.
pcb_places={'J1':(8,8,0),'U1':(25,20,0),'R1':(23,7,0),'R2':(39,9,0),
            'R3':(8,32,0),'C1':(46,24,0),'C2':(34,31,0),'C3':(18,34,0),'D1':(8,38,0)}
fpobjs={}
for ref,lib,name,val,libid,fp,desc in parts:
    libname,fpname=fp.split(':',1)
    f=pcbnew.FootprintLoad(f'/usr/share/kicad/footprints/{libname}.pretty',fpname)
    if f is None: raise RuntimeError('Could not load footprint '+fp)
    f.SetReference(ref); f.SetValue(val)
    x,y,rot=pcb_places[ref]
    f.SetPosition(vec(x,y)); f.SetOrientationDegrees(rot)
    board.Add(f); fpobjs[ref]=f

# Attach KiCad net objects to pads by the schematic pin/net table.
for ref, mapping in pinnets.items():
    f=fpobjs[ref]
    for pad in f.Pads():
        number=pad.GetNumber()
        if number in mapping: pad.SetNet(nets[mapping[number]])

# Track paths are specified in millimetres and use the plated through-hole pad centres.
# All GND pads are connected by the B.Cu ground pour, rather than long daisy-chain tracks.
def pad_xy(ref,num):
    p=next(p for p in fpobjs[ref].Pads() if p.GetNumber()==str(num))
    return (pcbnew.ToMM(p.GetPosition().x),pcbnew.ToMM(p.GetPosition().y))
def add_path(netname, points, layer, width=0.45):
    pts=[]
    for x,y in points:
        q=vec(x,y)
        if not pts or q!=pts[-1]: pts.append(q)
    for a,b in zip(pts,pts[1:]):
        t=pcbnew.PCB_TRACK(board); t.SetStart(a); t.SetEnd(b); t.SetWidth(iu(width)); t.SetLayer(layer); t.SetNet(nets[netname]); board.Add(t)
F=pcbnew.F_Cu; B=pcbnew.B_Cu

# +5 V distribution. Routes stay on the board's back side to leave the top side open for learning and probing.
add_path('+5V',[pad_xy('J1',1), (4,8), (4,4), (22,4), pad_xy('R1',1)],B,0.55)
add_path('+5V',[pad_xy('R1',1),(20,10),(18,18),(18,29),(25,29),pad_xy('U1',4)],B,0.55)
add_path('+5V',[pad_xy('U1',4),(18,31),pad_xy('C3',1)],B,0.45)
add_path('+5V',[pad_xy('U1',4),(18,30),(38,30),(38,20),pad_xy('U1',8)],B,0.55)
add_path('+5V',[pad_xy('U1',8),(35,21),(31,29),(25,34),pad_xy('C3',1)],B,0.45)

# Discharge node: R1/R2 junction and timer pin 7.
add_path('DISCH',[pad_xy('U1',7),(38,20.54),(38,7),pad_xy('R1',2)],F,0.4)
add_path('DISCH',[pad_xy('R1',2),(38,8.5),pad_xy('R2',1)],F,0.4)

# Timing node links pins 2 and 6, the R2 end, and the positive lead of C1.
add_path('TIMING',[pad_xy('U1',2),(20,19),(20,16),(44,16),(44,22),pad_xy('C1',1)],B,0.4)
add_path('TIMING',[pad_xy('U1',6),(34,25.08),(40,25.08),(40,20),(44,20),(44,22),pad_xy('C1',1)],B,0.4)
add_path('TIMING',[pad_xy('C1',1),(52,22),(52,10),pad_xy('R2',2)],B,0.4)

# Output and LED series path.
add_path('OUT',[pad_xy('U1',3),(22,28),(14,28),(14,32),pad_xy('R3',1)],F,0.55)
add_path('LED_A',[pad_xy('R3',2),(20.7,35),(13,35),(13,38),pad_xy('D1',2)],F,0.45)

# Control-voltage bypass capacitor, routed locally.
add_path('CTRL',[pad_xy('U1',5),(33.5,28.5),(33.5,30),pad_xy('C2',1)],F,0.35)

# Beginner-friendly polarity and interface legends on the front silkscreen.
for label,(x,y) in [('+5V',(5.0,4.2)),('GND',(12.0,4.2)),('LED',(5.0,42.3))]:
    txt=pcbnew.PCB_TEXT(board); txt.SetText(label); txt.SetPosition(vec(x,y)); txt.SetLayer(pcbnew.F_SilkS)
    txt.SetTextSize(vec(1.0,1.0)); txt.SetTextThickness(iu(0.15)); board.Add(txt)

# Board outline, 58 x 44 mm.
outline=[(1,1),(59,1),(59,45),(1,45),(1,1)]
for a,b in zip(outline,outline[1:]):
    s=pcbnew.PCB_SHAPE(); s.SetShape(pcbnew.SHAPE_T_SEGMENT); s.SetStart(vec(*a)); s.SetEnd(vec(*b)); s.SetLayer(pcbnew.Edge_Cuts); s.SetWidth(iu(0.05)); board.Add(s)

# A single B.Cu GND copper zone; plated THT pads provide layer-to-layer connection.
zone=pcbnew.ZONE(board); zone.SetLayer(B); zone.SetNet(nets['GND']); zone.SetLocalClearance(iu(0.3)); zone.SetThermalReliefGap(iu(0.3)); zone.SetThermalReliefSpokeWidth(iu(0.4)); zone.SetMinThickness(iu(0.25)); zone.SetIsRuleArea(False)
poly=zone.Outline(); poly.NewOutline()
for x,y in [(1.3,1.3),(58.7,1.3),(58.7,44.7),(1.3,44.7)]: poly.Append(iu(x),iu(y))
board.Add(zone)

board_path=ROOT/f'{PROJECT}.kicad_pcb'
pcbnew.SaveBoard(str(board_path),board)
# KiCad 7's Python zone filler is more stable after a fresh board reload than on a board
# assembled entirely through SWIG objects in the same interpreter.
board=pcbnew.LoadBoard(str(board_path))
filler=pcbnew.ZONE_FILLER(board)
filler.Fill(board.Zones())
board.BuildConnectivity()
unrouted=board.GetConnectivity().GetUnconnectedCount(False)
if unrouted:
    raise RuntimeError(f'PCB still has {unrouted} unrouted connections')
pcbnew.SaveBoard(str(board_path),board)
print('Wrote schematic, PCB, project, BOM, connections to',ROOT)
print('KiCad connectivity check: 0 unrouted connections after GND zone fill')
print('Pin geometry:', {ref:len(get_pins(lib,name)) for ref,lib,name,*_ in parts})
for ref,f in fpobjs.items():
    print(ref, {p.GetNumber(): tuple(round(pcbnew.ToMM(v),3) for v in (p.GetPosition().x,p.GetPosition().y)) for p in f.Pads()})
