# Apple Example Bot
# Name: Example Bot
# You must set move to teleport, east, west, south, north, northeast, northwest, southeast, or southwest to move in the respective directions.
# Any invalid move will be taken as no move.
# You have three types of sensors: stairs, bots, and wreckage
# STAIRS: the stairs are pointed to by x_dir and y_dir
# BOTS: You have 8 sensor zones; directly north, south, east and west of you (4) and the 

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



