EESchema Schematic File Version 4
LIBS:power
LIBS:device
LIBS:Timer
LIBS:Connector_Generic
EELAYER 29 0
EELAYER END
$Descr A4 11693 8268
Sheet 1 1
Title "LED Blinking Circuit Using PCB"
Date "2026-11-23"
Rev "1.0"
Comp "Educational Project"
Comment1 "NE555 astable multivibrator, 5 V supply"
Comment2 "KiCad legacy schematic compatible with KiCanvas"
$EndDescr
$Comp
L Timer:NE555D U1
U 1 1 1
P 5600 3500
F 0 "U1" H 5600 4081 50  0000 C CNN
F 1 "NE555D" H 5600 3990 50 0000 C CNN
	1    5600 3500
	1    0 0 -1
$EndComp
$Comp
L Device:R R1
U 1 1 2
P 4100 2550
F 0 "R1" H 4170 2596 50 0000 L CNN
F 1 "1k" H 4170 2505 50 0000 L CNN
	1    4100 2550
	1    0 0 -1
$EndComp
$Comp
L Device:R R2
U 1 1 3
P 4700 2550
F 0 "R2" H 4770 2596 50 0000 L CNN
F 1 "100k" H 4770 2505 50 0000 L CNN
	1    4700 2550
	1    0 0 -1
$EndComp
$Comp
L Device:C_Polarized C1
U 1 1 4
P 4700 4500
F 0 "C1" H 4818 4546 50 0000 L CNN
F 1 "10uF" H 4818 4455 50 0000 L CNN
	1    4700 4500
	1    0 0 -1
$EndComp
$Comp
L Device:R R3
U 1 1 5
P 7200 3500
F 0 "R3" V 6993 3500 50 0000 C CNN
F 1 "330R" V 7084 3500 50 0000 C CNN
	1    7200 3500
	0    1 1 0
$EndComp
$Comp
L Device:LED D1
U 1 1 6
P 7900 3500
F 0 "D1" H 7893 3245 50 0000 C CNN
F 1 "RED LED" H 7893 3336 50 0000 C CNN
	1    7900 3500
	-1   0 0 1
$EndComp
$Comp
L Device:C C2
U 1 1 7
P 6800 4300
F 0 "C2" H 6915 4346 50 0000 L CNN
F 1 "10nF" H 6915 4255 50 0000 L CNN
	1    6800 4300
	1    0 0 -1
$EndComp
$Comp
L Device:C C3
U 1 1 8
P 7500 2400
F 0 "C3" H 7615 2446 50 0000 L CNN
F 1 "100nF" H 7615 2355 50 0000 L CNN
	1    7500 2400
	1    0 0 -1
$EndComp
$Comp
L Connector_Generic:Conn_01x02 J1
U 1 1 9
P 2700 3500
F 0 "J1" H 2618 3717 50 0000 C CNN
F 1 "5V INPUT" H 2618 3626 50 0000 C CNN
	1    2700 3500
	-1   0 0 -1
$EndComp
$Comp
L power:VCC #PWR01
U 1 1 10
P 3500 2100
F 0 "#PWR01" H 3500 1950 50 0001 C CNN
F 1 "VCC" H 3515 2273 50 0000 C CNN
	1    3500 2100
	1    0 0 -1
$EndComp
$Comp
L power:GND #PWR02
U 1 1 11
P 5600 5100
F 0 "#PWR02" H 5600 4850 50 0001 C CNN
F 1 "GND" H 5605 4927 50 0000 C CNN
	1    5600 5100
	1    0 0 -1
$EndComp
Wire Wire Line
	2900 3500 3500 3500
Wire Wire Line
	3500 3500 3500 2100
Wire Wire Line
	3500 2300 4100 2300
Wire Wire Line
	4100 2300 4100 2400
Wire Wire Line
	4100 2700 4100 3100
Wire Wire Line
	4100 3100 4700 3100
Wire Wire Line
	4700 2700 4700 3100
Wire Wire Line
	4700 3100 5200 3100
Wire Wire Line
	4700 2400 4700 2300
Wire Wire Line
	4700 2300 5600 2300
Wire Wire Line
	5600 2300 5600 3100
Wire Wire Line
	5200 3500 4700 3500
Wire Wire Line
	4700 3500 4700 4350
Wire Wire Line
	4700 3500 4700 4400
Wire Wire Line
	5200 3900 5200 4900
Wire Wire Line
	5200 4900 5600 4900
Wire Wire Line
	5600 3900 5600 5100
Wire Wire Line
	6000 3500 7050 3500
Wire Wire Line
	7350 3500 7750 3500
Wire Wire Line
	8050 3500 8500 3500
Wire Wire Line
	8500 3500 8500 4900
Wire Wire Line
	8500 4900 5600 4900
Wire Wire Line
	5600 2300 7500 2300
Wire Wire Line
	7500 2250 7500 2300
Wire Wire Line
	7500 2550 7500 4900
Wire Wire Line
	6000 3900 6800 3900
Wire Wire Line
	6800 3900 6800 4150
Wire Wire Line
	6800 4450 6800 4900
Wire Wire Line
	2900 3600 3200 3600
Wire Wire Line
	3200 3600 3200 4900
Wire Wire Line
	3200 4900 5600 4900
Wire Wire Line
	5600 4900 5600 5100
Connection ~ 4700 3100
Connection ~ 4700 3500
Connection ~ 5600 2300
Connection ~ 5600 4900
Text Notes 2500 1850 0 80 ~ 16
LED Blinking Circuit Using PCB
Text Notes 2500 2000 0 50 ~ 0
NE555 astable oscillator — 5 V regulated input
Text Notes 6950 3200 0 50 ~ 0
Output indicator
Text Notes 3900 5000 0 50 ~ 0
Timing capacitor return
$EndSCHEMATC
