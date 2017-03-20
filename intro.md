# ROBOTS

You're a robot trapped in a factory full of malfunctioning robots! You must run away from the robots because if they touch you it will destroy you. (They're mean robots!) Going downstairs to the next level of the factory can buy you some time. Fortunately, you have use of several sensors and can also teleport.

# Rules

Robots always run directly towards the player.

Robots will not step on staircases.

If robots crash into each other, they will leave a scrap heap behind.

If robots touch a scrap heap, they are destroyed.

If a robot touches a player, or a player touches a scrap heap, the game is over.

Points are awarded in the following ways:
 * one point per turn survived
 * (10 * level_num) for reaching the stairs
 * 10 points every time a robot crashes

# Motion

The player robot can move in 8 directions: `north`, `east`, `south`, `west`, `northeast`, `southeast`, `southwest` and `northwest`. The player can also `teleport` (teleporting can result in landing on a robot).

# Sensors

The player robot has many sensor variables it can use to help inform its moves.

**Stairs**: the variables `x_dir` and `y_dir` th pointed to the closest apple in the Apple Hunt game now point to the stairs.

**Robots**: the variables `sense_X` where `X` is one of `n`, `s`, `e`, `w`, `ne`, `nw`, `se`, or `sw` store the distance to the robot closest to the player in the given sensor area. The four cardinal sensors are in a direct line vertically or horizontally with the player. The four diagonal sensor zones are the remaining square areas in between the four cardinal direction sensors.

Example:
```
if sense_ne < 0 {
	move = southeast
}
```
Note that Little Python now supports the inequality comparison operators `<`,`>;`, `<=` and `>=`.

**Wreckage**: When robots crash they leave behind wreckage that will destroy other robots. These are like pits in the Apple Hunt game. Accordingly, there are 8 sensors that test the adjacent cells for wreckage. Those sensors are named `junk_X` where `X` is one of `n`, `s`, `e`, `w`, `ne`, `nw`, `se`, or `sw`. 

Example:
```
if junk_e {
	move = west
}
```


