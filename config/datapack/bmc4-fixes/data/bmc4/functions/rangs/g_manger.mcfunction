# Généré par config/rangs/generer.py depuis config/rangs/rangs.toml : ne pas
# modifier à la main.

# /feed (KubeJS le renvoie ici) ou /trigger bmc4_manger : rang 6 et plus.
execute unless score @s bmc4_rangs matches 6.. run tellraw @s ["", {"text": "/feed refusé : ", "color": "red"}, {"text": "il s'obtient au rang ", "color": "red"}, {"text": "⬩ Nétherite", "color": "#6B6B6B", "bold": false}, {"text": ". ", "color": "red"}, {"text": "Voir ce qu'il te manque : ", "color": "gray"}, {"text": "[Où j'en suis]", "color": "aqua", "bold": true, "clickEvent": {"action": "run_command", "value": "/prestige"}, "hoverEvent": {"action": "show_text", "contents": "Ton rang, le suivant, ce qu'il te manque"}}]
execute if score @s bmc4_rangs matches 6.. run function bmc4:rangs/manger
scoreboard players set @s bmc4_manger 0
