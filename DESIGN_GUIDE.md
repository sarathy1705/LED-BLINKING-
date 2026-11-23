# NE555 LED Blinker — KiCad design guide

This project is a 5 V NE555 astable blinker with a red LED, a 2-pin power connector, three resistors, and three capacitors. The schematic and PCB are included in the project folder. The [connection diagram](connection_diagram.svg) shows the circuit functionally; the KiCad schematic carries a labelled net for every pin.

## Timing calculation

For the standard NE555 astable connection, the timing capacitor charges through R1 and R2, then discharges through R2. The manufacturer’s equations are `tHIGH ≈ 0.693 × (R1 + R2) × C`, `tLOW ≈ 0.693 × R2 × C`, and `f ≈ 1.44 / ((R1 + 2R2) × C)`. The timer capacitor swings approximately between one-third and two-thirds of VCC. [1]

With R1 = 1 kΩ, R2 = 10 kΩ, and C = 100 µF:

- `tHIGH ≈ 0.693 × 11,000 × 0.0001 = 0.762 s`
- `tLOW ≈ 0.693 × 10,000 × 0.0001 = 0.693 s`
- `T ≈ 1.455 s`, so `f ≈ 0.687 Hz` (about 0.69 blinks per second)
- The output is high about 52.4% of each cycle.

The blink should be slow and easy to see. The NE555 operating range includes 5 V; TI lists 4.5 V as the minimum recommended supply for NE555 variants. [1]

## Circuit connections to verify before PCB work

Use these named nets to check the schematic or exported netlist:

| Net | Pins/components on the net |
| --- | --- |
| `+5V` | J1 pin 1; U1 pins 4 (RESET) and 8 (VCC); R1 pin 1; C3 pin 1 |
| `GND` | J1 pin 2; U1 pin 1; D1 pin 1 (K/cathode); C1, C2, and C3 pin 2 |
| `DISCH` | U1 pin 7; R1 pin 2; R2 pin 1 |
| `TIMING` | U1 pins 2 and 6; R2 pin 2; C1 pin 1 (positive) |
| `CTRL` | U1 pin 5; C2 pin 1 |
| `OUT` | U1 pin 3; R3 pin 1 |
| `LED_A` | R3 pin 2; D1 pin 2 (A/anode) |

C1 is polarized: its positive lead is on `TIMING`; its negative lead is on ground. The red LED’s anode faces the 220 Ω resistor and output pin 3. Its cathode returns to ground. C2 is the 10 nF control-voltage bypass at pin 5. C3 is the 100 nF decoupling capacitor directly between +5 V and ground.

## Parts and KiCad library names

Use the exact library identifiers below. These are official KiCad symbol and footprint library names. Generic symbols are paired with footprints separately in the schematic workflow. [2] [3]

| Ref. | Symbol | Value | Footprint |
| --- | --- | --- | --- |
| U1 | `Timer:NE555P` | NE555P | `Package_DIP:DIP-8_W7.62mm` |
| R1 | `Device:R` | 1k | `Resistor_THT:R_Axial_DIN0309_L9.0mm_D3.2mm_P12.70mm_Horizontal` |
| R2 | `Device:R` | 10k | `Resistor_THT:R_Axial_DIN0309_L9.0mm_D3.2mm_P12.70mm_Horizontal` |
| R3 | `Device:R` | 220 | `Resistor_THT:R_Axial_DIN0309_L9.0mm_D3.2mm_P12.70mm_Horizontal` |
| C1 | `Device:C_Polarized` | 100uF, use a 10 V or higher rating | `Capacitor_THT:CP_Radial_D5.0mm_P2.00mm` |
| C2 | `Device:C` | 10nF | `Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm` |
| C3 | `Device:C` | 100nF | `Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm` |
| D1 | `Device:LED` | LED_RED | `LED_THT:LED_D5.0mm` |
| J1 | `Connector_Generic:Conn_01x02` | 5V INPUT | `TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2_1x02_P5.00mm_Horizontal` |

The 5.00 mm screw-terminal footprint is a real THT Phoenix-style pattern. Before ordering, check that the specific terminal block you buy has a 5.00 mm pitch and a compatible body size. Likewise, confirm the actual electrolytic’s body diameter and lead pitch; choose a larger radial footprint if the purchased part does not fit.

## Open the supplied KiCad project

1. Extract the project archive if using the ZIP. In KiCad’s Project Manager, choose **File → Open Project…** and open `NE555_LED_Blinker.kicad_pro` or the project folder. If you are creating it from scratch instead, choose **File → New Project**, enter `NE555_LED_Blinker`, and save it in a new folder.
2. Open `NE555_LED_Blinker.kicad_sch` in the Schematic Editor. The symbols, values, footprints, and named nets are already populated in the supplied schematic. If rebuilding from scratch, press **A** to add the symbols listed above, then press **E** on each symbol to set its reference, value, and footprint.
3. Add the 2-pin connector as `J1`; label pin 1 `+5V` and pin 2 `GND`. Connect U1 pin 4 to +5 V, not left floating. Join pins 2 and 6, then connect that joined timing node to R2 pin 2 and C1 positive.
4. Connect R1 from +5 V to pin 7. Connect R2 from pin 7 to the joined pins 2/6. Connect pin 3 through R3 (220 Ω) to D1 anode; connect D1 cathode to ground.
5. Connect C2 (10 nF) from pin 5 to ground. Connect C3 (100 nF) between +5 V and ground near the timer. Connect C1 negative to ground.
6. Add the `Power:+5V` and `Power:GND` symbols where useful. Add `Power:PWR_FLAG` on the incoming +5 V and ground rails if ERC reports that an externally supplied rail is not driven by a power-output pin. KiCad’s guide describes power flags as the standard way to tell ERC that an external source powers those rails. [2]
7. Choose **Tools → Annotate Schematic** if references need numbering. Check that there is only one U1, R1–R3, C1–C3, D1, and J1. Save.
8. Run **Inspect → Electrical Rules Checker** and **Run ERC**. Correct every unintended missing connection, unconnected pin, or undriven power warning. A power flag is a modelling hint for ERC; it is not a physical component or power source. ERC verifies schematic-rule consistency, not whether the circuit performs as intended. [2]
9. Export a netlist and inspect it before making a PCB. Confirm that U1 pins 2 and 6 appear on the same net with R2 pin 2 and C1 pin 1. Also confirm that pin 7 shares a net only with R1 pin 2 and R2 pin 1. The included `netlist.net` shows the project’s current connections.

## Build or review the PCB

1. Open `NE555_LED_Blinker.kicad_pcb` in PCB Editor. To create a new board from a schematic, open PCB Editor and choose **Tools → Update PCB from Schematic** (F8), accept the changes, and place the footprints. KiCad’s documented workflow uses this update step to transfer components and nets. [2]
2. Use `Package_DIP:DIP-8_W7.62mm` for U1. Align the package notch with pin 1. Keep C3 close to U1 pins 8 and 1. Keep C1 close to pins 2 and 6. Place R1/R2 close to pin 7. Put the power terminal at the edge of the board with its `+5V` and `GND` labels next to the correct pads.
3. Draw a closed rectangle on **Edge.Cuts**. The supplied outline is about 58 × 44 mm. Leave clearance between the copper outline, tracks, and edge.
4. Route by net. A beginner-friendly starting point is 0.30–0.35 mm for low-current signal tracks and 0.50–0.60 mm for +5 V and LED current paths, with at least 0.25 mm clearance if supported by your board fabricator. Check that these values meet the fabricator’s minimum rules. This design uses a two-layer board with a ground pour on B.Cu; it avoids the extra jumpers that a single-copper-layer version may need.
5. Add a GND copper zone on B.Cu, assign it to `GND`, and press **B** to refill zones after moving or routing anything. Verify that the zone connects to each ground pad and is not split into disconnected islands.
6. Run **Inspect → Design Rules Checker**. Fix all unconnected items, shorts, clearance errors, silkscreen overlaps, and board-outline errors. KiCad 7.0.11 was available for file generation in this environment, but its command-line interface does not provide ERC or DRC commands. The schematic’s netlist exported successfully and KiCad’s board connectivity engine reported 0 unrouted connections after the GND zone fill; however, a full ERC/DRC report was not produced here. Please run both checks in your desktop KiCad before fabrication. The supplied PCB is a starting placement and routing, not a substitute for reviewing the final DRC report in the exact KiCad/fabricator setup you will use.

## Simulate and test

The capacitor voltage repeatedly charges from roughly one-third to two-thirds of the supply through R1 + R2. At the upper threshold, the timer output goes low and its discharge path turns on; the capacitor discharges through R2. At the lower threshold, the output returns high and the LED lights through R3. This repeats continuously. [1]

For a bench test, set a current-limited supply to 5.0 V before connecting it. With the supply off, check for a short between +5 V and GND, confirm the electrolytic stripe/negative lead goes to ground, and confirm the LED flat side/cathode goes to ground. Apply power and measure the connector: approximately 5 V should appear between +5 V and GND. The LED should flash about once every 1.46 seconds. A multimeter in DC-voltage mode on the timing capacitor should show a changing voltage; a basic meter may average the cycling signal rather than display its waveform. Never place a current meter directly across the supply.

If the LED stays off, first check connector polarity, U1 orientation, pin 4 RESET voltage, LED polarity, and the resistor path from pin 3. If it stays on, check that pins 2 and 6 are joined and that R2 is connected between the timing node and pin 7. If the timing capacitor stays near 0 V, inspect C1 polarity, the pin 7/R2 junction, and solder bridges. Also confirm the timing capacitor is really 100 µF rather than 100 nF. If the circuit is erratic, check the 100 nF supply bypass at U1 and keep the timing-capacitor loop short.

## Manufacturing exports

Gerber copper, solder-mask, silkscreen, and Edge.Cuts layers are in `manufacturing/`. The folder also contains separate plated and non-plated Excellon drill files and drill maps. The schematic PDF, BOM, pin-to-net CSV, and STEP model are alongside the KiCad files. `3D_Render_KiCad_Raytracing.png` is a screenshot captured from KiCad 7’s native 3D Viewer with raytracing enabled and the board’s library component models visible. The STEP file contains the board body, but KiCad 7’s STEP exporter cannot convert the library’s VRML-only component models, so it does not include component bodies. Open the native board in KiCad’s 3D Viewer to inspect component orientation and clearances visually before fabrication.

The assembled-board render requirement is now included. KiCad’s connectivity engine reported 0 unrouted connections after the GND zone fill, but this is not a full DRC result. Neither ERC nor DRC reports were produced in this environment, and the design has not been electrically bench-tested. Do not send the Gerbers to a fab until ERC and DRC have been run in desktop KiCad, any findings reviewed and corrected, and the physical parts’ footprints matched to their manufacturers’ drawings.

## References

[1]: https://www.ti.com/lit/ds/symlink/ne555.pdf "Texas Instruments NE555/NA555/SA555/SE555 datasheet"
[2]: https://docs.kicad.org/9.0/en/getting_started_in_kicad/getting_started_in_kicad.html "KiCad 9 Getting Started guide"
[3]: https://gitlab.com/kicad/libraries "Official KiCad symbol and footprint libraries"
