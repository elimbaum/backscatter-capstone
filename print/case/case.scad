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
switch_big_hole_diam = 4.1;
switch_small_hole_diam = 2.7;
switch_hole_height = 1.8;

// confirm location from datasheet
switch_small_hole_location = [-3, 3];
switch_big_hole_location = [-9.5, 2.5];

// arduino  holes

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
    
    // minkowski() {
    //     square([arduino.x + switch_arduino_sep + rf_switch.x,
    //             arduino.y);
    //     circle(5);
    // }
    
    // cube([case_border * 2 + arduino.x + switch_arduino_sep + rf_switch.x,
    //     case_border + arduino.y + case_border,
    //     case_thickness + arduino.z]);
}

module holes() {
    // arduino holes

    // rf switch holes
    translate([arduino.x + switch_arduino_sep + rf_switch.x,
                    (arduino.y - rf_switch.y)/2, 0])
    {
        translate(switch_small_hole_location) {
            linear_extrude(case_thickness + switch_hole_height) {
                circle(d=switch_small_hole_diam);
            }
        }

        translate(switch_big_hole_location) {
            linear_extrude(case_thickness + switch_hole_height) {
                circle(d=switch_big_hole_diam);
            }
        }
    }
}

union() {
    difference() {
        case_outline();
        components();
    }
    holes();
}


// case_outline();

