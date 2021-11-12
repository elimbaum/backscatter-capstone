// units: mm
// x/y coordinates with USB port on left.

$fs = 0.01;

TOL = 0.001;

FULL = 10;

rf_switch = [19.07, 45.29, 2.6];
arduino = [68.61, 53.34, 3.6];

switch_arduino_sep = 10;

// underneath arduino
case_thickness = 3;

// border around arduino
case_border = 5;

// switch info
switch_hole_diam = 2.6;

switch_hole_location = [-2.92, 2.79];

// actually 3.2mm
arduino_hole_diam = 3;

// orientation: USB/pwr on left
arduino_hole_locations = [
    // lower left
    [14.0, 2.5],

    // lower right (outcrop)
    [66.1, 7.6],

    // upper right (outcrop)
    [66.1, 35.5],

    // upper left
    [15.3, 50.7]
];

text_depth = 0.5;

module components() {
    translate([0, 0, case_thickness]) {
        cube([arduino.x, arduino.y, FULL]);

        translate([arduino.x + switch_arduino_sep,
                    (arduino.y - rf_switch.y)/2, 0]) {
            cube([rf_switch.x, rf_switch.y, FULL]);
        }
    }
}

module case_outline() {
    linear_extrude(case_thickness + arduino.z) {
        minkowski() {
            square([arduino.x + switch_arduino_sep + rf_switch.x,
                    arduino.y]);
            circle(case_border);
        }

    }
}

module rf_hole() {
    cylinder(r = switch_hole_diam/2,
             h = case_thickness + rf_switch.z);
}

module arduino_hole() {
    cylinder(r = arduino_hole_diam/2,
             h = case_thickness + arduino.z);
}

module all_holes() {

    // arduino holes

    // rf switch holes
    translate([arduino.x + switch_arduino_sep + rf_switch.x,
                    (arduino.y - rf_switch.y)/2, 0])
    {
        translate(switch_hole_location) {
            rf_hole();
            translate([0, rf_switch.y - 2 * switch_hole_location.y, 0]) {
                rf_hole();
            }
        }
    }

    for (h=arduino_hole_locations) {
        translate(h) {
            arduino_hole();
        }
    }
}

module elitext() {
    translate([case_border + arduino.x,
                arduino.y/2,
                case_thickness + arduino.z - text_depth])
    rotate(90) {
        linear_extrude(text_depth + TOL)
        text("ebaum // backscatter v1",
                size=3,
                halign="center",
                valign="center");
    }
}

union() {
    difference() {
        case_outline();
        components();
        elitext();
    }
    all_holes();
}

