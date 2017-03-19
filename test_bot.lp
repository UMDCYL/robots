# Apple Example Bot
# Name: Example Bot
# You must set move to east, west, south, or north to move in the respective directions.
# Any invalid move will be taken as no move.
# LEVEL 1: Two variables you have access to are x_dir and y_dir to the nearest apple
# x_dir will be set to 0, east, or west
# y_dir will be set to 0, north, or south
# LEVEL 2: Advanced: check for pit traps with pit_to_east, pit_to_west, pit_to_south or pit_to_north!

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


# once we can test for < and > these should be changed.
# I'd also like to do something like:
# sense_dist = sense_n + sense_s + sense_e + sense_w + sense_nw + sense_ne + sense_se + sense_sw
# if sense_dist < 3 {
#	move = teleport
# }
# ...  but for now this serviceable for testing

if (sense_n is 3) {
    move = teleport
}

if (sense_s is 3) {
    move = teleport
}

if (sense_e is 3) {
    move = teleport
}

if (sense_w is 3) {
    move = teleport
}

if (sense_ne is 3) {
    move = teleport
}

if (sense_nw is 3) {
    move = teleport
}

if (sense_sw is 3) {
    move = teleport
}

if (sense_se is 3) {
    move = teleport
}
