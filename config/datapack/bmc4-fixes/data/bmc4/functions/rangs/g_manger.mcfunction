# Généré par config/rangs/generer.py depuis config/rangs/rangs.toml : ne pas
# modifier à la main.

# /trigger bmc4_manger (ou /feed, que KubeJS renvoie ici) : rang 6 et plus.
execute unless score @s bmc4_rangs matches 6.. run tellraw @s ["", {"text": "/feed refusé : ", "color": "red"}, {"text": "il s'obtient au rang ", "color": "red"}, {"text": "⬩ Nétherite", "color": "#6B6B6B", "bold": false}, {"text": ". ", "color": "red"}, {"text": "Voir ton rang : /trigger bmc4_rang set 2", "color": "gray"}]
execute if score @s bmc4_rangs matches 6.. run function bmc4:rangs/manger
scoreboard players set @s bmc4_manger 0
