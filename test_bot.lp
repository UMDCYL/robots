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

jump = 3

if sense_n and sense_n < jump {
	move = teleport
}

if sense_ne and sense_ne < jump {
	move = teleport
}

if sense_nw and sense_nw < jump {
	move = teleport
}

if sense_s and sense_s < jump {
	move = teleport
}

if sense_sw and sense_sw < jump {
	move = teleport
}

if sense_se and sense_se < jump {
	move = teleport
}

if sense_e and sense_e < jump {
	move = teleport
}

if sense_w and sense_w < jump {
	move = teleport
}

if junk_e and move is east {
	move = teleport
}

if junk_w and move is west {
	move = teleport
}

if junk_n and move is north {
	move = teleport
}

if junk_s and move is south {
	move = teleport
}
	
if junk_ne and move is northeast {
	move = teleport
}

if junk_nw and move is northwest {
	move = teleport
}
	
if junk_se and move is southeast {
	move = teleport
}

if junk_sw and move is southwest {
	move = teleport
}



