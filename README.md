# LED Blinking Circuit Using PCB

This project is a complete educational design for a 5 V LED blinker built on a single-sided PCB using an NE555/LM555 timer in astable mode.

## Included files

- `main.pdf` — polished project report suitable for submission or printing.
- `main.typ` — editable Typst report source.
- `circuit.svg` — editable circuit illustration used in the report.
- `LED_Blinking_Circuit.sch` — KiCad legacy schematic; it can be opened by KiCad and uploaded to KiCanvas.
- `LED_Blinking_Circuit.kicad_sch` — KiCad 6+ native schematic reference file for direct KiCanvas viewing.
- `LED_Blinking_Circuit.kicad_pcb` — native KiCad PCB layout with footprints, board outline, labels, nets, and tracks.
- `LED_Blinking_Circuit.kicad_pro` — minimal KiCad project metadata.

## Design summary

- Supply: regulated 5 V DC
- Timer: NE555 or LM555, DIP-8
- Timing values: R1 = 1 kΩ, R2 = 100 kΩ, C1 = 10 µF
- LED resistor: R3 = 330 Ω
- Nominal frequency: approximately 0.72 Hz
- Nominal period: approximately 1.39 s
- LED: 5 mm red through-hole LED

## Open in KiCad

1. Download and unzip the project package.
2. Open `LED_Blinking_Circuit.kicad_pcb` in KiCad PCB Editor to inspect or edit the board.
3. Open `LED_Blinking_Circuit.kicad_sch` in KiCad Schematic Editor for the KiCad 6+ reference view, or open `LED_Blinking_Circuit.sch` for the legacy symbol-and-wire schematic and convert it when prompted.
4. Before manufacturing, run KiCad's electrical rules check and confirm the footprint assignments and final routing.

## Open in KiCanvas online

1. Open the KiCanvas website: https://kicanvas.org/
2. Choose the option to open or upload a local file.
3. Upload `LED_Blinking_Circuit.kicad_pcb` to view the PCB layout in the browser.
4. Upload `LED_Blinking_Circuit.kicad_sch` to view the KiCad 6+ schematic reference in the browser. KiCanvas does not parse KiCad 5 legacy `.sch` files, so use the native `.kicad_sch` file for online viewing.

The `.kicad_pcb` and `.kicad_sch` files are the browser-viewable artifacts. KiCanvas does not require the project archive or a local KiCad installation to inspect them. KiCanvas is an early-alpha viewer, so use desktop KiCad for final electrical-rule checks and manufacturing output.

## Building the PDF

Install Typst and run:

```bash
typst compile main.typ main.pdf
```

The report contains a bill of materials, PCB layout recommendations, assembly procedure, test table, fault-finding guide, safety notes, conclusion, and viva questions.

## Important customization

Replace `Student Project` and the generated date in `main.typ` if the report must carry a particular student name, class, institution, or submission date. Fill in the measured-value column in the testing section after assembling the board.
