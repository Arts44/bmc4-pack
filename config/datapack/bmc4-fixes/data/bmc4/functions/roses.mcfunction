# Retire les roses de Wither autour de la base.
#
# Chaque mob tué par un Wither en laisse une. Elles infligent le
# Flétrissement à tout ce qui les touche — les dragons errent sur
# huit blocs et finissent par marcher dedans.
#
# fill plafonne à 32768 blocs par appel. Un cube de 200 × 40 × 200
# en ferait 1,6 million : on découpe en tranches de 50 × 40 × 50,
# soit 100 000 par tranche… encore trop.
#
# On passe donc par des tranches de 32 blocs de haut sur 31 × 31,
# ce qui tient largement, et on couvre la zone en damier.

say === NETTOYAGE DES ROSES DE WITHER ===

# Centre : la base, -4200 / 5920. Couverture Y 50 à 90.
fill -4300 50 5820 -4270 90 5850 air replace minecraft:wither_rose
fill -4269 50 5820 -4239 90 5850 air replace minecraft:wither_rose
fill -4238 50 5820 -4208 90 5850 air replace minecraft:wither_rose
fill -4207 50 5820 -4177 90 5850 air replace minecraft:wither_rose
fill -4176 50 5820 -4146 90 5850 air replace minecraft:wither_rose
fill -4145 50 5820 -4115 90 5850 air replace minecraft:wither_rose
fill -4114 50 5820 -4100 90 5850 air replace minecraft:wither_rose

fill -4300 50 5851 -4270 90 5881 air replace minecraft:wither_rose
fill -4269 50 5851 -4239 90 5881 air replace minecraft:wither_rose
fill -4238 50 5851 -4208 90 5881 air replace minecraft:wither_rose
fill -4207 50 5851 -4177 90 5881 air replace minecraft:wither_rose
fill -4176 50 5851 -4146 90 5881 air replace minecraft:wither_rose
fill -4145 50 5851 -4115 90 5881 air replace minecraft:wither_rose
fill -4114 50 5851 -4100 90 5881 air replace minecraft:wither_rose

fill -4300 50 5882 -4270 90 5912 air replace minecraft:wither_rose
fill -4269 50 5882 -4239 90 5912 air replace minecraft:wither_rose
fill -4238 50 5882 -4208 90 5912 air replace minecraft:wither_rose
fill -4207 50 5882 -4177 90 5912 air replace minecraft:wither_rose
fill -4176 50 5882 -4146 90 5912 air replace minecraft:wither_rose
fill -4145 50 5882 -4115 90 5912 air replace minecraft:wither_rose
fill -4114 50 5882 -4100 90 5912 air replace minecraft:wither_rose

fill -4300 50 5913 -4270 90 5943 air replace minecraft:wither_rose
fill -4269 50 5913 -4239 90 5943 air replace minecraft:wither_rose
fill -4238 50 5913 -4208 90 5943 air replace minecraft:wither_rose
fill -4207 50 5913 -4177 90 5943 air replace minecraft:wither_rose
fill -4176 50 5913 -4146 90 5943 air replace minecraft:wither_rose
fill -4145 50 5913 -4115 90 5943 air replace minecraft:wither_rose
fill -4114 50 5913 -4100 90 5943 air replace minecraft:wither_rose

fill -4300 50 5944 -4270 90 5974 air replace minecraft:wither_rose
fill -4269 50 5944 -4239 90 5974 air replace minecraft:wither_rose
fill -4238 50 5944 -4208 90 5974 air replace minecraft:wither_rose
fill -4207 50 5944 -4177 90 5974 air replace minecraft:wither_rose
fill -4176 50 5944 -4146 90 5974 air replace minecraft:wither_rose
fill -4145 50 5944 -4115 90 5974 air replace minecraft:wither_rose
fill -4114 50 5944 -4100 90 5974 air replace minecraft:wither_rose

fill -4300 50 5975 -4270 90 6005 air replace minecraft:wither_rose
fill -4269 50 5975 -4239 90 6005 air replace minecraft:wither_rose
fill -4238 50 5975 -4208 90 6005 air replace minecraft:wither_rose
fill -4207 50 5975 -4177 90 6005 air replace minecraft:wither_rose
fill -4176 50 5975 -4146 90 6005 air replace minecraft:wither_rose
fill -4145 50 5975 -4115 90 6005 air replace minecraft:wither_rose
fill -4114 50 5975 -4100 90 6005 air replace minecraft:wither_rose

say === FIN DU NETTOYAGE ===
