# Robots Example Bot
# Name: SirRobin
# You must set move to teleport, east, west, south, north, northeast, northwest, southeast, or southwest to move in the respective directions.
# Any invalid move will be taken as no move.
# You have three types of sensors: stairs, bots, and wreckage
# STAIRS: the stairs are pointed to by x_dir and y_dir
# BOTS: You have 8 sensor zones; directly north, south, east and west of you and the remaining diagonal regions (sense_n, sense_e, sense_w, sense_s, sense_ne, sense_nw, sense_se, sense_sw). The value of the sensor is the distance to the closest bot in the sensor. (Please note LP supports the inequality operators >, <, >=, and <=.
# WRECKAGE: When bots crash, they leave wreckage. The var 'junk_X' is set to 1 when wreckage is directly adjacent to the player (where X is one of n, s, e, w, ne, se, sw, or se).

if x_dir is east {
  move = east
}
if x_dir is west {
  move = west
}
if y_dir is north {
  move = north
}
if y_dir is south {
  move = south
}

if x_dir is east and y_dir is north {
    move = northeast
}

if x_dir is east and y_dir is south {
    move = southeast
}

if x_dir is west and y_dir is north {
    move = northwest
}

if x_dir is west and y_dir is south {
    move = southwest
}

if (sense_n > 0 and sense_n < 3) {
    move = teleport
}

if (sense_s > 0 and sense_s < 3) {
    move = teleport
}

if (sense_e > 0 and sense_e < 3) {
    move = teleport
}

if (sense_w > 0 and sense_w < 3) {
    move = teleport
}

if (sense_ne > 0 and sense_ne < 3) {
    move = teleport
}

if (sense_se > 0 and sense_se < 3) {
    move = teleport
}

if (sense_sw > 0 and sense_sw < 3) {
    move = teleport
}

if (sense_nw > 0 and sense_nw < 3) {
    move = teleport
}

if (junk_s and move is south) {
    move = teleport
}

if (junk_n and move is north) {
    move = teleport
}

if (junk_e and move is east) {
    move = teleport
}

if (junk_w and move is west) {
    move = teleport
}

if (junk_ne and move is northeast) {
    move = teleport
}

if (junk_se and move is southeast) {
    move = teleport
}

if (junk_nw and move is northwest) {
    move = teleport
}

if (junk_sw and move is southwest) {
    move = teleport
}
