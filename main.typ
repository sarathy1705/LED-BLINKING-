// LED Blinking Circuit Using PCB — native report
#import "report-theme.typ": report-accent, report-theme

#show: report-theme.with(
  title: "LED Blinking Circuit Using PCB",
  author: "Student Project",
  rhythm: "report",
  running-header: true,
)

#page(margin: (top: 30%, x: 2.2cm), numbering: none, header: none)[
  #set par(first-line-indent: 0em)
  #align(center)[
    #text(size: 26pt, weight: "bold", fill: report-accent)[LED Blinking Circuit Using PCB]
    #v(0.5em)
    #text(size: 14pt, fill: luma(80))[Design, construction, testing and analysis of a 555-timer astable multivibrator]
    #v(2em)
    #line(length: 40%, stroke: 0.5pt + luma(160))
    #v(2em)
    #text(size: 12pt)[
      Prepared by: Student Project \
      Date: #datetime.today().display("[year]-[month]-[day]")
    ]
  ]
]

#page(numbering: none, header: none)[
  #outline(title: [Table of Contents], indent: 1.5em)
]
#counter(page).update(1)

= Abstract

This project presents the design and construction of a continuously blinking light-emitting diode (LED) circuit on a printed circuit board (PCB). An NE555 timer is configured as an astable multivibrator, so it repeatedly charges and discharges a timing capacitor. The resulting square-wave output drives a red LED through a current-limiting resistor. The circuit is inexpensive, operates from a regulated 5 V supply, and is suitable for demonstrating timing, oscillation, soldering, PCB assembly, and electronic testing.

The selected component values give a nominal blink frequency of approximately 0.69 Hz, corresponding to a period of about 1.45 s. The LED therefore remains visibly ON for about 0.76 s and OFF for about 0.69 s. Practical measurements may differ because of component tolerance, supply variation, LED characteristics, and the 555 timer's output behavior.

= Introduction

A blinking LED is a simple but useful electronic application. It converts an electrical timing signal into a visible indication and is commonly used in status indicators, warning lamps, educational trainers, and embedded systems. A PCB implementation is more reliable and repeatable than a loose breadboard because the interconnections are fixed, mechanically supported, and easier to inspect.

This project uses the classic 555 timer in astable mode. No external microcontroller or programming is required. The timing network contains two resistors and one capacitor; changing any of these values changes the blink rate. The completed board can be powered by a regulated 5 V USB supply or a laboratory DC supply.

= Objectives

- Design a stable LED blinking circuit using a 555 timer.
- Calculate the timing components for a visible blink rate.
- Prepare a practical single-sided PCB layout with clear component labels.
- Assemble the board using through-hole components and soldering.
- Test supply voltage, LED current, output waveform, and blink frequency.
- Compare theoretical results with practical measurements.

= Principle of Operation

In astable mode, the 555 timer has no stable state. The timing capacitor $C_1$ charges through $R_1 + R_2$ until its voltage reaches approximately two-thirds of the supply voltage. The timer output then changes state and the discharge transistor turns on. The capacitor discharges through $R_2$ until its voltage falls to approximately one-third of the supply voltage. The output changes state again, the discharge transistor turns off, and the cycle repeats.

The output at pin 3 is connected to LED $D_1$ through resistor $R_3$. When the output is high, current flows through the LED and it glows. When the output is low, the LED is off. Capacitor $C_2$ filters the control-voltage pin, while capacitor $C_3$ provides local supply decoupling and reduces false triggering caused by supply noise.

#figure(
  image("circuit.svg", width: 100%),
  caption: [555-timer astable LED blinker schematic.]
) <fig-schematic>

= Circuit Design and Calculations

== Component selection

The design targets a blink rate close to 0.7 Hz. The following values are inexpensive, commonly available, and suitable for through-hole PCB assembly:

#table(
  columns: (2.3cm, 2.5cm, 4.7cm),
  inset: 7pt,
  fill: (_, row) => if calc.odd(row) { luma(245) } else { white },
  [*Reference*], [*Value*], [*Purpose*],
  [R1], [1 kΩ], [Limits the minimum charging resistance.],
  [R2], [100 kΩ], [Sets most of the timing period.],
  [C1], [10 µF], [Main timing capacitor.],
  [R3], [330 Ω], [Limits current through the LED.],
  [C2], [10 nF], [Filters the control pin.],
  [C3], [100 nF], [Decouples the 5 V supply at the IC.],
  [D1], [5 mm red LED], [Visual output indicator.],
  [IC1], [NE555 or LM555], [Astable timer.],
)

== Timing equations

For a 555 timer in astable operation:

$ t_"ON" = 0.693 (R_1 + R_2) C_1 $

$ t_"OFF" = 0.693 R_2 C_1 $

$ T = t_"ON" + t_"OFF" = 0.693 (R_1 + 2R_2) C_1 $

$ f = 1/T $

Using $R_1 = 1 "kΩ"$, $R_2 = 100 "kΩ"$, and $C_1 = 10 "µF"$:

$ t_"ON" = 0.693 (101000)(10 × 10^(-6)) ≈ 0.700 "s" $

$ t_"OFF" = 0.693 (100000)(10 × 10^(-6)) ≈ 0.693 "s" $

$ T ≈ 1.393 "s", quad f ≈ 0.718 "Hz" $

The duty cycle is:

$ D = t_"ON"/T × 100 ≈ 50.3% $

The LED current is limited by $R_3$. Assuming a high output of approximately 4.5 V and a red LED forward voltage of 2.0 V:

$ I_"LED" ≈ (4.5 - 2.0)/330 ≈ 7.6 "mA" $

This current is bright enough for an indicator while remaining below the typical continuous rating of a 5 mm LED.

= PCB Design and Construction

== PCB layout recommendations

The board may be made as a single-sided through-hole PCB approximately 60 mm × 45 mm. Place the NE555 near the center so timing traces remain short. Keep $C_3$ within 10–15 mm of the IC's VCC and GND pins. Place the LED and its resistor at the board edge for visibility. Use a wider trace for the supply rails and maintain clear polarity markings for the LED, electrolytic capacitor, and power connector.

Recommended layout rules:

- Use 0.6–0.8 mm signal tracks and 1.0–1.2 mm tracks for the supply rails.
- Keep the timing node joining pins 2 and 6 compact and away from the LED output trace.
- Add a two-pin input connector labelled `+5V` and `GND`.
- Mark pin 1 of the 555 socket and the cathode stripe of electrolytic capacitors.
- Provide a test point at pin 3 for observing the output waveform.
- Use a socket for the IC so it can be replaced without desoldering.

== Bill of materials

#table(
  columns: (1.4cm, 2.9cm, 2.4cm, 2.8cm),
  inset: 7pt,
  fill: (_, row) => if calc.odd(row) { luma(245) } else { white },
  [*Qty.*], [*Component*], [*Specification*], [*PCB note*],
  [1], [NE555 / LM555 IC], [DIP-8], [Fit in an 8-pin socket.],
  [1], [DIP-8 socket], [Through-hole], [Install before IC.],
  [1], [R1], [1 kΩ, ¼ W], [Colour code or printed body.],
  [1], [R2], [100 kΩ, ¼ W], [Timing resistor.],
  [1], [R3], [330 Ω, ¼ W], [LED current limit.],
  [1], [C1], [10 µF, ≥16 V], [Observe polarity.],
  [1], [C2], [10 nF ceramic], [Control pin filter.],
  [1], [C3], [100 nF ceramic], [Place near IC.],
  [1], [D1], [5 mm red LED], [Long lead is anode.],
  [1], [2-pin connector], [5 V input], [Mark polarity.],
  [1], [PCB], [Single-sided], [Approx. 60 mm × 45 mm.],
)

== Assembly procedure

1. Inspect the PCB for shorted tracks, incomplete etching, or un-drilled holes.
2. Solder the wire links or zero-ohm links first, if the chosen single-sided layout requires them.
3. Solder the resistors, then the IC socket, ceramic capacitors, connector, LED, and electrolytic capacitor.
4. Trim component leads and inspect every solder joint under good lighting.
5. Check continuity between the 5 V rail and ground. There must not be a direct short circuit.
6. Insert the 555 IC with its notch aligned with the socket marking.
7. Apply a regulated 5 V supply with a current limit of approximately 100 mA.
8. Confirm that the LED blinks and record the test results.

= Testing and Results

The board should be tested before it is enclosed. A suitable test table is shown below; the measured-value column can be completed during laboratory testing.

#table(
  columns: (3.2cm, 3.2cm, 3.2cm),
  inset: 7pt,
  fill: (_, row) => if calc.odd(row) { luma(245) } else { white },
  [*Test*], [*Expected value*], [*Measured value*],
  [Supply voltage], [5.0 V DC], [not measured],
  [Supply current], [Typically 10–30 mA], [not measured],
  [LED ON time], [About 0.70 s], [not measured],
  [LED OFF time], [About 0.69 s], [not measured],
  [Period], [About 1.39 s], [not measured],
  [Frequency], [About 0.72 Hz], [not measured],
  [Output at pin 3], [Square wave, 0–5 V], [not measured],
)

A multimeter can verify the supply voltage and approximate current. An oscilloscope connected to pin 3 can display the square wave and provide accurate period and duty-cycle measurements. If an oscilloscope is unavailable, count the number of blinks in one minute and calculate $f = N/60$, where $N$ is the number of complete blink cycles.

= Fault Finding

If the LED remains permanently OFF, first check LED polarity, the continuity of the output trace, the orientation of the IC, and the presence of 5 V at pin 8. If the LED remains permanently ON, check for a short around pins 2 and 6, an incorrectly inserted timing capacitor, or a damaged 555. If the LED blinks very rapidly or very slowly, verify the values and units of $R_2$ and $C_1$; a 100 nF capacitor accidentally fitted in place of 10 µF changes the frequency by approximately two orders of magnitude.

If the circuit resets or flickers when a nearby load is switched, improve supply decoupling, shorten the supply wires, and confirm that the source is regulated. A socketed IC and clearly labelled test points make troubleshooting faster and reduce the chance of PCB damage.

= Safety and Good Practice

Use only a regulated low-voltage DC supply. Do not connect the board directly to mains voltage. Observe capacitor polarity, avoid solder bridges, and allow the soldering iron to cool on its stand. Use eye protection when cutting component leads. Disconnect power before modifying the board. The circuit is intended as a low-voltage educational project and should not be used as a safety-critical indicator without further design review.

= Advantages, Limitations and Applications

The circuit is low cost, easy to understand, and works without software. Its PCB form is robust and can be reused as a timing demonstrator. The main limitation is that the blink frequency depends on resistor and capacitor tolerances and is not as precise as a crystal-controlled or microcontroller-based design. The 555 output also has different source and sink characteristics, so the LED current calculation is approximate.

Typical applications include power-on indicators, warning flashers, classroom demonstrations, simple signal beacons, toy circuits, and introductory PCB workshops. Replacing $C_1$ with a potentiometer or selecting a different capacitor allows the blink rate to be adjusted.

= Conclusion

A practical LED blinking circuit was designed around a 555 timer, calculated for a nominal frequency of about 0.72 Hz, and specified for assembly on a compact single-sided PCB. The design demonstrates the complete workflow from circuit theory to component selection, PCB layout, soldering, testing, and fault finding. The final board provides a reliable visual indication and a useful foundation for more advanced timer, sensor, and microcontroller projects.

= References

1. Texas Instruments, *LM555 Timer Datasheet*, sections on astable operation and electrical characteristics.
2. Horowitz and Hill, *The Art of Electronics*, 3rd edition, timer and oscillator fundamentals.
3. Standard NE555 application notes covering astable multivibrator timing equations.

#pagebreak()
= Appendix A — Quick Build Checklist

#table(
  columns: (0.9cm, 8.7cm),
  inset: 7pt,
  fill: (_, row) => if calc.odd(row) { luma(245) } else { white },
  [*✓*], [*Checkpoint*],
  [☐], [All component values match the bill of materials.],
  [☐], [IC notch and electrolytic capacitor polarity are marked.],
  [☐], [LED anode and cathode are correctly identified.],
  [☐], [No solder bridge exists between +5 V and GND.],
  [☐], [Supply is regulated to 5 V before connection.],
  [☐], [LED flashes at a visibly regular rate.],
  [☐], [Measured results are recorded in the testing table.],
)

= Appendix B — Suggested Viva Questions

- Why is the 555 called an astable multivibrator in this circuit?
- What is the role of $R_2$ and $C_1$ in setting the frequency?
- Why is a resistor connected in series with the LED?
- What would happen if the value of $C_1$ were doubled?
- Why should the 100 nF decoupling capacitor be placed close to the IC?
- What is the difference between a breadboard implementation and a PCB implementation?
