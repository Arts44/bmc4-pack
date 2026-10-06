# Rapporte la position d'Arts_Vio en la stockant dans un
# tableau de score : « scoreboard players get » est journalisé,
# contrairement à « data get ».

scoreboard objectives add bmc4_pos dummy

execute store result score X bmc4_pos run data get entity Arts_Vio Pos[0] 1
execute store result score Y bmc4_pos run data get entity Arts_Vio Pos[1] 1
execute store result score Z bmc4_pos run data get entity Arts_Vio Pos[2] 1

say === POSITION ===
scoreboard players get X bmc4_pos
scoreboard players get Y bmc4_pos
scoreboard players get Z bmc4_pos
