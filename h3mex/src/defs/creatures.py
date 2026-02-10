from enum import IntEnum


class Disposition(IntEnum):
    Compliant = 0
    Friendly = 1
    Aggressive = 2
    Hostile = 3
    Savage = 4
    Precise = 5


class ID(IntEnum):
    LEVEL_7_PLUS = 65521
    LEVEL_7 = 65522
    LEVEL_6_PLUS = 65523
    LEVEL_6 = 65524
    LEVEL_5_PLUS = 65525
    LEVEL_5 = 65526
    LEVEL_4_PLUS = 65527
    LEVEL_4 = 65528
    LEVEL_3_PLUS = 65529
    LEVEL_3 = 65530
    LEVEL_2_PLUS = 65531
    LEVEL_2 = 65532
    LEVEL_1_PLUS = 65533
    LEVEL_1 = 65534
    NONE = 65535  # 2 bytes max

    Pikeman = 0
    Halberdier = 1
    Archer = 2
    Marksman = 3
    Griffin = 4
    Royal_Griffin = 5
    Swordsman = 6
    Crusader = 7
    Monk = 8
    Zealot = 9
    Cavalier = 10
    Champion = 11
    Angel = 12
    Archangel = 13
    Centaur = 14
    Centaur_Captain = 15
    Dwarf = 16
    Battle_Dwarf = 17
    Wood_Elf = 18
    Grand_Elf = 19
    Pegasus = 20
    Silver_Pegasus = 21
    Dendroid_Guard = 22
    Dendroid_Soldier = 23
    Unicorn = 24
    War_Unicorn = 25
    Green_Dragon = 26
    Gold_Dragon = 27
    Gremlin = 28
    Master_Gremlin = 29
    Stone_Gargoyle = 30
    Obsidian_Gargoyle = 31
    Stone_Golem = 32
    Iron_Golem = 33
    Mage = 34
    Arch_Mage = 35
    Genie = 36
    Master_Genie = 37
    Naga = 38
    Naga_Queen = 39
    Giant = 40
    Titan = 41
    Imp = 42
    Familiar = 43
    Gog = 44
    Magog = 45
    Hell_Hound = 46
    Cerberus = 47
    Demon = 48
    Horned_Demon = 49
    Pit_Fiend = 50
    Pit_Lord = 51
    Efreeti = 52
    Efreet_Sultan = 53
    Devil = 54
    Arch_Devil = 55
    Skeleton = 56
    Skeleton_Warrior = 57
    Walking_Dead = 58
    Zombie = 59
    Wight = 60
    Wraith = 61
    Vampire = 62
    Vampire_Lord = 63
    Lich = 64
    Power_Lich = 65
    Black_Knight = 66
    Dread_Knight = 67
    Bone_Dragon = 68
    Ghost_Dragon = 69
    Troglodyte = 70
    Infernal_Troglodyte = 71
    Harpy = 72
    Harpy_Hag = 73
    Beholder = 74
    Evil_Eye = 75
    Medusa = 76
    Medusa_Queen = 77
    Minotaur = 78
    Minotaur_King = 79
    Manticore = 80
    Scorpicore = 81
    Red_Dragon = 82
    Black_Dragon = 83
    Goblin = 84
    Hobgoblin = 85
    Wolf_Rider = 86
    Wolf_Raider = 87
    Orc = 88
    Orc_Chieftain = 89
    Ogre = 90
    Ogre_Mage = 91
    Roc = 92
    Thunderbird = 93
    Cyclops = 94
    Cyclops_King = 95
    Behemoth = 96
    Ancient_Behemoth = 97
    Gnoll = 98
    Gnoll_Marauder = 99
    Lizardman = 100
    Lizard_Warrior = 101
    Gorgon = 102
    Mighty_Gorgon = 103
    Serpent_Fly = 104
    Dragon_Fly = 105
    Basilisk = 106
    Greater_Basilisk = 107
    Wyvern = 108
    Wyvern_Monarch = 109
    Hydra = 110
    Chaos_Hydra = 111
    Air_Elemental = 112
    Earth_Elemental = 113
    Fire_Elemental = 114
    Water_Elemental = 115
    Gold_Golem = 116
    Diamond_Golem = 117
    Pixie = 118
    Sprite = 119
    Psychic_Elemental = 120
    Magic_Elemental = 121
    NOT_USED_1 = 122
    Ice_Elemental = 123
    NOT_USED_2 = 124
    Magma_Elemental = 125
    NOT_USED_3 = 126
    Storm_Elemental = 127
    NOT_USED_4 = 128
    Energy_Elemental = 129
    Firebird = 130
    Phoenix = 131
    Azure_Dragon = 132
    Crystal_Dragon = 133
    Faerie_Dragon = 134
    Rust_Dragon = 135
    Enchanter = 136
    Sharpshooter = 137
    Halfling = 138
    Peasant = 139
    Boar = 140
    Mummy = 141
    Nomad = 142
    Rogue = 143
    Troll = 144
    Catapult = 145
    Ballista = 146
    First_Aid_Tent = 147
    Ammo_Cart = 148
    Arrow_Tower = 149
    Cannon = 150
    Sea_Dog = 151
    Electric_Tower = 152
    Nymph = 153
    Oceanid = 154
    Crew_Mate = 155
    Seaman = 156
    Pirate = 157
    Corsair = 158
    Stormbird = 159
    Ayssid = 160
    Sea_Witch = 161
    Sorceress = 162
    Nix = 163
    Nix_Warrior = 164
    Sea_Serpent = 165
    Haspid = 166
    Satyr = 167
    Fangarm = 168
    Leprechaun = 169
    Steel_Golem = 170
    Halfling_Grenadier = 171
    Mechanic = 172
    Engineer = 173
    Armadillo = 174
    Bellwether_Armadillo = 175
    Automaton = 176
    Sentinel_Automaton = 177
    Sandworm = 178
    Olgoi_Khorkhoi = 179
    Gunslinger = 180
    Bounty_Hunter = 181
    Couatl = 182
    Crimson_Couatl = 183
    Dreadnought = 184
    Juggernaut = 185
    Kobold = 186
    Kobold_Foreman = 187
    Mountain_Ram = 188
    Argali = 189
    Snow_Elf = 190
    Steel_Elf = 191
    Yeti = 192
    Yeti_Runemaster = 193
    Shaman = 194
    Great_Shaman = 195
    Mammoth = 196
    War_Mammoth = 197
    Jotunn = 198
    Jotunn_Warlord = 199


class Castle(IntEnum):
    Pikeman = ID.Pikeman
    Halberdier = ID.Halberdier
    Archer = ID.Archer
    Marksman = ID.Marksman
    Griffin = ID.Griffin
    Royal_Griffin = ID.Royal_Griffin
    Swordsman = ID.Swordsman
    Crusader = ID.Crusader
    Monk = ID.Monk
    Zealot = ID.Zealot
    Cavalier = ID.Cavalier
    Champion = ID.Champion
    Angel = ID.Angel
    Archangel = ID.Archangel


class Rampart(IntEnum):
    Centaur = ID.Centaur
    Centaur_Captain = ID.Centaur_Captain
    Dwarf = ID.Dwarf
    Battle_Dwarf = ID.Battle_Dwarf
    Wood_Elf = ID.Wood_Elf
    Grand_Elf = ID.Grand_Elf
    Pegasus = ID.Pegasus
    Silver_Pegasus = ID.Silver_Pegasus
    Dendroid_Guard = ID.Dendroid_Guard
    Dendroid_Soldier = ID.Dendroid_Soldier
    Unicorn = ID.Unicorn
    War_Unicorn = ID.War_Unicorn
    Green_Dragon = ID.Green_Dragon
    Gold_Dragon = ID.Gold_Dragon


class Tower(IntEnum):
    Gremlin = ID.Gremlin
    Master_Gremlin = ID.Master_Gremlin
    Stone_Gargoyle = ID.Stone_Gargoyle
    Obsidian_Gargoyle = ID.Obsidian_Gargoyle
    Stone_Golem = ID.Stone_Golem
    Iron_Golem = ID.Iron_Golem
    Mage = ID.Mage
    Arch_Mage = ID.Arch_Mage
    Genie = ID.Genie
    Master_Genie = ID.Master_Genie
    Naga = ID.Naga
    Naga_Queen = ID.Naga_Queen
    Giant = ID.Giant
    Titan = ID.Titan


class Inferno(IntEnum):
    Imp = ID.Imp
    Familiar = ID.Familiar
    Gog = ID.Gog
    Magog = ID.Magog
    Hell_Hound = ID.Hell_Hound
    Cerberus = ID.Cerberus
    Demon = ID.Demon
    Horned_Demon = ID.Horned_Demon
    Pit_Fiend = ID.Pit_Fiend
    Pit_Lord = ID.Pit_Lord
    Efreeti = ID.Efreeti
    Efreet_Sultan = ID.Efreet_Sultan
    Devil = ID.Devil
    Arch_Devil = ID.Arch_Devil


class Necropolis(IntEnum):
    Skeleton = ID.Skeleton
    Skeleton_Warrior = ID.Skeleton_Warrior
    Walking_Dead = ID.Walking_Dead
    Zombie = ID.Zombie
    Wight = ID.Wight
    Wraith = ID.Wraith
    Vampire = ID.Vampire
    Vampire_Lord = ID.Vampire_Lord
    Lich = ID.Lich
    Power_Lich = ID.Power_Lich
    Black_Knight = ID.Black_Knight
    Dread_Knight = ID.Dread_Knight
    Bone_Dragon = ID.Bone_Dragon
    Ghost_Dragon = ID.Ghost_Dragon


class Dungeon(IntEnum):
    Troglodyte = ID.Troglodyte
    Infernal_Troglodyte = ID.Infernal_Troglodyte
    Harpy = ID.Harpy
    Harpy_Hag = ID.Harpy_Hag
    Beholder = ID.Beholder
    Evil_Eye = ID.Evil_Eye
    Medusa = ID.Medusa
    Medusa_Queen = ID.Medusa_Queen
    Minotaur = ID.Minotaur
    Minotaur_King = ID.Minotaur_King
    Manticore = ID.Manticore
    Scorpicore = ID.Scorpicore
    Red_Dragon = ID.Red_Dragon
    Black_Dragon = ID.Black_Dragon


class Stronghold(IntEnum):
    Goblin = ID.Goblin
    Hobgoblin = ID.Hobgoblin
    Wolf_Rider = ID.Wolf_Rider
    Wolf_Raider = ID.Wolf_Raider
    Orc = ID.Orc
    Orc_Chieftain = ID.Orc_Chieftain
    Ogre = ID.Ogre
    Ogre_Mage = ID.Ogre_Mage
    Roc = ID.Roc
    Thunderbird = ID.Thunderbird
    Cyclops = ID.Cyclops
    Cyclops_King = ID.Cyclops_King
    Behemoth = ID.Behemoth
    Ancient_Behemoth = ID.Ancient_Behemoth


class Fortress(IntEnum):
    Gnoll = ID.Gnoll
    Gnoll_Marauder = ID.Gnoll_Marauder
    Lizardman = ID.Lizardman
    Lizard_Warrior = ID.Lizard_Warrior
    Gorgon = ID.Gorgon
    Mighty_Gorgon = ID.Mighty_Gorgon
    Serpent_Fly = ID.Serpent_Fly
    Dragon_Fly = ID.Dragon_Fly
    Basilisk = ID.Basilisk
    Greater_Basilisk = ID.Greater_Basilisk
    Wyvern = ID.Wyvern
    Wyvern_Monarch = ID.Wyvern_Monarch
    Hydra = ID.Hydra
    Chaos_Hydra = ID.Chaos_Hydra


class Conflux(IntEnum):
    Pixie = ID.Pixie
    Sprite = ID.Sprite
    Air_Elemental = ID.Air_Elemental
    Storm_Elemental = ID.Storm_Elemental
    Water_Elemental = ID.Water_Elemental
    Ice_Elemental = ID.Ice_Elemental
    Fire_Elemental = ID.Fire_Elemental
    Energy_Elemental = ID.Energy_Elemental
    Earth_Elemental = ID.Earth_Elemental
    Magma_Elemental = ID.Magma_Elemental
    Psychic_Elemental = ID.Psychic_Elemental
    Magic_Elemental = ID.Magic_Elemental
    Firebird = ID.Firebird
    Phoenix = ID.Phoenix


class Cove(IntEnum):
    Oceanid = ID.Oceanid
    Crew_Mate = ID.Crew_Mate
    Seaman = ID.Seaman
    Pirate = ID.Pirate
    Corsair = ID.Corsair
    Sea_Dog = ID.Sea_Dog
    Stormbird = ID.Stormbird
    Ayssid = ID.Ayssid
    Sea_Witch = ID.Sea_Witch
    Sorceress = ID.Sorceress
    Nix = ID.Nix
    Nix_Warrior = ID.Nix_Warrior
    Sea_Serpent = ID.Sea_Serpent
    Haspid = ID.Haspid


class Factory(IntEnum):
    Halfling = ID.Halfling
    Halfling_Grenadier = ID.Halfling_Grenadier
    Mechanic = ID.Mechanic
    Engineer = ID.Engineer
    Armadillo = ID.Armadillo
    Bellwether_Armadillo = ID.Bellwether_Armadillo
    Automaton = ID.Automaton
    Sentinel_Automaton = ID.Sentinel_Automaton
    Sandworm = ID.Sandworm
    Olgoi_Khorkhoi = ID.Olgoi_Khorkhoi
    Gunslinger = ID.Gunslinger
    Bounty_Hunter = ID.Bounty_Hunter
    Couatl = ID.Couatl
    Crimson_Couatl = ID.Crimson_Couatl
    Dreadnought = ID.Dreadnought
    Juggernaut = ID.Juggernaut


class Bulwark(IntEnum):
    Kobold = ID.Kobold
    Kobold_Foreman = ID.Kobold_Foreman
    Mountain_Ram = ID.Mountain_Ram
    Argali = ID.Argali
    Snow_Elf = ID.Snow_Elf
    Steel_Elf = ID.Steel_Elf
    Yeti = ID.Yeti
    Yeti_Runemaster = ID.Yeti_Runemaster
    Shaman = ID.Shaman
    Great_Shaman = ID.Great_Shaman
    Mammoth = ID.Mammoth
    War_Mammoth = ID.War_Mammoth
    Jotunn = ID.Jotunn
    Jotunn_Warlord = ID.Jotunn_Warlord


class Neutral(IntEnum):
    Peasant = ID.Peasant
    Boar = ID.Boar
    Rogue = ID.Rogue
    Leprechaun = ID.Leprechaun
    Mummy = ID.Mummy
    Nomad = ID.Nomad
    Sharpshooter = ID.Sharpshooter
    Satyr = ID.Satyr
    Steel_Golem = ID.Steel_Golem
    Troll = ID.Troll
    Gold_Golem = ID.Gold_Golem
    Fangarm = ID.Fangarm
    Diamond_Golem = ID.Diamond_Golem
    Enchanter = ID.Enchanter
    Faerie_Dragon = ID.Faerie_Dragon
    Rust_Dragon = ID.Rust_Dragon
    Crystal_Dragon = ID.Crystal_Dragon
    Azure_Dragon = ID.Azure_Dragon


class Level1(IntEnum):
    Pikeman = ID.Pikeman
    Halberdier = ID.Halberdier
    Centaur = ID.Centaur
    Centaur_Captain = ID.Centaur_Captain
    Gremlin = ID.Gremlin
    Master_Gremlin = ID.Master_Gremlin
    Imp = ID.Imp
    Familiar = ID.Familiar
    Skeleton = ID.Skeleton
    Skeleton_Warrior = ID.Skeleton_Warrior
    Troglodyte = ID.Troglodyte
    Infernal_Troglodyte = ID.Infernal_Troglodyte
    Goblin = ID.Goblin
    Hobgoblin = ID.Hobgoblin
    Gnoll = ID.Gnoll
    Gnoll_Marauder = ID.Gnoll_Marauder
    Pixie = ID.Pixie
    Sprite = ID.Sprite
    Nymph = ID.Nymph
    Oceanid = ID.Oceanid
    Halfling = ID.Halfling
    Halfling_Grenadier = ID.Halfling_Grenadier
    Kobold = ID.Kobold
    Kobold_Foreman = ID.Kobold_Foreman
    Peasant = ID.Peasant


class Level2(IntEnum):
    Archer = ID.Archer
    Marksman = ID.Marksman
    Dwarf = ID.Dwarf
    Battle_Dwarf = ID.Battle_Dwarf
    Stone_Gargoyle = ID.Stone_Gargoyle
    Obsidian_Gargoyle = ID.Obsidian_Gargoyle
    Gog = ID.Gog
    Magog = ID.Magog
    Walking_Dead = ID.Walking_Dead
    Zombie = ID.Zombie
    Harpy = ID.Harpy
    Harpy_Hag = ID.Harpy_Hag
    Wolf_Rider = ID.Wolf_Rider
    Wolf_Raider = ID.Wolf_Raider
    Lizardman = ID.Lizardman
    Lizard_Warrior = ID.Lizard_Warrior
    Air_Elemental = ID.Air_Elemental
    Storm_Elemental = ID.Storm_Elemental
    Crew_Mate = ID.Crew_Mate
    Seaman = ID.Seaman
    Mechanic = ID.Mechanic
    Engineer = ID.Engineer
    Mountain_Ram = ID.Mountain_Ram
    Argali = ID.Argali
    Boar = ID.Boar
    Rogue = ID.Rogue
    Leprechaun = ID.Leprechaun


class Level3(IntEnum):
    Griffin = ID.Griffin
    Royal_Griffin = ID.Royal_Griffin
    Wood_Elf = ID.Wood_Elf
    Grand_Elf = ID.Grand_Elf
    Stone_Golem = ID.Stone_Golem
    Iron_Golem = ID.Iron_Golem
    Hell_Hound = ID.Hell_Hound
    Cerberus = ID.Cerberus
    Wight = ID.Wight
    Wraith = ID.Wraith
    Beholder = ID.Beholder
    Evil_Eye = ID.Evil_Eye
    Orc = ID.Orc
    Orc_Chieftain = ID.Orc_Chieftain
    Serpent_Fly = ID.Serpent_Fly
    Dragon_Fly = ID.Dragon_Fly
    Water_Elemental = ID.Water_Elemental
    Ice_Elemental = ID.Ice_Elemental
    Pirate = ID.Pirate
    Corsair = ID.Corsair
    Armadillo = ID.Armadillo
    Bellwether_Armadillo = ID.Bellwether_Armadillo
    Snow_Elf = ID.Snow_Elf
    Steel_Elf = ID.Steel_Elf
    Mummy = ID.Mummy
    Nomad = ID.Nomad
    Sea_Dog = ID.Sea_Dog


class Level4(IntEnum):
    Swordsman = ID.Swordsman
    Crusader = ID.Crusader
    Pegasus = ID.Pegasus
    Silver_Pegasus = ID.Silver_Pegasus
    Mage = ID.Mage
    Arch_Mage = ID.Arch_Mage
    Demon = ID.Demon
    Horned_Demon = ID.Horned_Demon
    Vampire = ID.Vampire
    Vampire_Lord = ID.Vampire_Lord
    Medusa = ID.Medusa
    Medusa_Queen = ID.Medusa_Queen
    Ogre = ID.Ogre
    Ogre_Mage = ID.Ogre_Mage
    Basilisk = ID.Basilisk
    Greater_Basilisk = ID.Greater_Basilisk
    Fire_Elemental = ID.Fire_Elemental
    Energy_Elemental = ID.Energy_Elemental
    Stormbird = ID.Stormbird
    Ayssid = ID.Ayssid
    Automaton = ID.Automaton
    Sentinel_Automaton = ID.Sentinel_Automaton
    Yeti = ID.Yeti
    Yeti_Runemaster = ID.Yeti_Runemaster
    Sharpshooter = ID.Sharpshooter
    Satyr = ID.Satyr
    Steel_Golem = ID.Steel_Golem


class Level5(IntEnum):
    Monk = ID.Monk
    Zealot = ID.Zealot
    Dendroid_Guard = ID.Dendroid_Guard
    Dendroid_Soldier = ID.Dendroid_Soldier
    Genie = ID.Genie
    Master_Genie = ID.Master_Genie
    Pit_Fiend = ID.Pit_Fiend
    Pit_Lord = ID.Pit_Lord
    Lich = ID.Lich
    Power_Lich = ID.Power_Lich
    Minotaur = ID.Minotaur
    Minotaur_King = ID.Minotaur_King
    Roc = ID.Roc
    Thunderbird = ID.Thunderbird
    Gorgon = ID.Gorgon
    Mighty_Gorgon = ID.Mighty_Gorgon
    Earth_Elemental = ID.Earth_Elemental
    Magma_Elemental = ID.Magma_Elemental
    Sea_Witch = ID.Sea_Witch
    Sorceress = ID.Sorceress
    Sandworm = ID.Sandworm
    Olgoi_Khorkhoi = ID.Olgoi_Khorkhoi
    Shaman = ID.Shaman
    Great_Shaman = ID.Great_Shaman
    Troll = ID.Troll
    Gold_Golem = ID.Gold_Golem
    Fangarm = ID.Fangarm


class Level6(IntEnum):
    Cavalier = ID.Cavalier
    Champion = ID.Champion
    Unicorn = ID.Unicorn
    War_Unicorn = ID.War_Unicorn
    Naga = ID.Naga
    Naga_Queen = ID.Naga_Queen
    Efreeti = ID.Efreeti
    Efreet_Sultan = ID.Efreet_Sultan
    Black_Knight = ID.Black_Knight
    Dread_Knight = ID.Dread_Knight
    Manticore = ID.Manticore
    Scorpicore = ID.Scorpicore
    Cyclops = ID.Cyclops
    Cyclops_King = ID.Cyclops_King
    Wyvern = ID.Wyvern
    Wyvern_Monarch = ID.Wyvern_Monarch
    Psychic_Elemental = ID.Psychic_Elemental
    Magic_Elemental = ID.Magic_Elemental
    Nix = ID.Nix
    Nix_Warrior = ID.Nix_Warrior
    Gunslinger = ID.Gunslinger
    Bounty_Hunter = ID.Bounty_Hunter
    Mammoth = ID.Mammoth
    War_Mammoth = ID.War_Mammoth
    Diamond_Golem = ID.Diamond_Golem
    Enchanter = ID.Enchanter


class Level7(IntEnum):
    Angel = ID.Angel
    Archangel = ID.Archangel
    Green_Dragon = ID.Green_Dragon
    Gold_Dragon = ID.Gold_Dragon
    Giant = ID.Giant
    Titan = ID.Titan
    Devil = ID.Devil
    Arch_Devil = ID.Arch_Devil
    Bone_Dragon = ID.Bone_Dragon
    Ghost_Dragon = ID.Ghost_Dragon
    Red_Dragon = ID.Red_Dragon
    Black_Dragon = ID.Black_Dragon
    Behemoth = ID.Behemoth
    Ancient_Behemoth = ID.Ancient_Behemoth
    Hydra = ID.Hydra
    Chaos_Hydra = ID.Chaos_Hydra
    Firebird = ID.Firebird
    Phoenix = ID.Phoenix
    Azure_Dragon = ID.Azure_Dragon
    Crystal_Dragon = ID.Crystal_Dragon
    Faerie_Dragon = ID.Faerie_Dragon
    Rust_Dragon = ID.Rust_Dragon
    Sea_Serpent = ID.Sea_Serpent
    Haspid = ID.Haspid
    Couatl = ID.Couatl
    Crimson_Couatl = ID.Crimson_Couatl
    Dreadnought = ID.Dreadnought
    Juggernaut = ID.Juggernaut
    Jotunn = ID.Jotunn
    Jotunn_Warlord = ID.Jotunn_Warlord


VALUE = {
    ID.Pikeman: 80,
    ID.Halberdier: 115,
    ID.Archer: 126,
    ID.Marksman: 184,
    ID.Griffin: 351,
    ID.Royal_Griffin: 448,
    ID.Swordsman: 445,
    ID.Crusader: 588,
    ID.Monk: 582,
    ID.Zealot: 750,
    ID.Cavalier: 1946,
    ID.Champion: 2100,
    ID.Angel: 5019,
    ID.Archangel: 8776,
    ID.Centaur: 100,
    ID.Centaur_Captain: 138,
    ID.Dwarf: 138,
    ID.Battle_Dwarf: 209,
    ID.Wood_Elf: 234,
    ID.Grand_Elf: 331,
    ID.Pegasus: 518,
    ID.Silver_Pegasus: 532,
    ID.Dendroid_Guard: 517,
    ID.Dendroid_Soldier: 803,
    ID.Unicorn: 1806,
    ID.War_Unicorn: 2030,
    ID.Green_Dragon: 4872,
    ID.Gold_Dragon: 8613,
    ID.Gremlin: 44,
    ID.Master_Gremlin: 66,
    ID.Stone_Gargoyle: 165,
    ID.Obsidian_Gargoyle: 201,
    ID.Stone_Golem: 250,
    ID.Iron_Golem: 412,
    ID.Mage: 570,
    ID.Arch_Mage: 680,
    ID.Genie: 884,
    ID.Master_Genie: 942,
    ID.Naga: 2016,
    ID.Naga_Queen: 2840,
    ID.Giant: 3718,
    ID.Titan: 7500,
    ID.Imp: 50,
    ID.Familiar: 60,
    ID.Gog: 159,
    ID.Magog: 240,
    ID.Hell_Hound: 357,
    ID.Cerberus: 392,
    ID.Demon: 445,
    ID.Horned_Demon: 480,
    ID.Pit_Fiend: 765,
    ID.Pit_Lord: 1224,
    ID.Efreeti: 1670,
    ID.Efreet_Sultan: 2343,
    ID.Devil: 5101,
    ID.Arch_Devil: 7115,
    ID.Skeleton: 60,
    ID.Skeleton_Warrior: 85,
    ID.Walking_Dead: 98,
    ID.Zombie: 128,
    ID.Wight: 252,
    ID.Wraith: 315,
    ID.Vampire: 555,
    ID.Vampire_Lord: 783,
    ID.Lich: 848,
    ID.Power_Lich: 1079,
    ID.Black_Knight: 2087,
    ID.Dread_Knight: 2382,
    ID.Bone_Dragon: 3388,
    ID.Ghost_Dragon: 4696,
    ID.Troglodyte: 59,
    ID.Infernal_Troglodyte: 84,
    ID.Harpy: 154,
    ID.Harpy_Hag: 238,
    ID.Beholder: 336,
    ID.Evil_Eye: 367,
    ID.Medusa: 517,
    ID.Medusa_Queen: 577,
    ID.Minotaur: 835,
    ID.Minotaur_King: 1068,
    ID.Manticore: 1547,
    ID.Scorpicore: 1589,
    ID.Red_Dragon: 4702,
    ID.Black_Dragon: 8721,
    ID.Goblin: 60,
    ID.Hobgoblin: 78,
    ID.Wolf_Rider: 130,
    ID.Wolf_Raider: 203,
    ID.Orc: 192,
    ID.Orc_Chieftain: 240,
    ID.Ogre: 416,
    ID.Ogre_Mage: 672,
    ID.Roc: 1027,
    ID.Thunderbird: 1106,
    ID.Cyclops: 1266,
    ID.Cyclops_King: 1443,
    ID.Behemoth: 3162,
    ID.Ancient_Behemoth: 6168,
    ID.Gnoll: 56,
    ID.Gnoll_Marauder: 90,
    ID.Lizardman: 126,
    ID.Lizard_Warrior: 156,
    ID.Serpent_Fly: 268,
    ID.Dragon_Fly: 312,
    ID.Basilisk: 552,
    ID.Greater_Basilisk: 714,
    ID.Gorgon: 890,
    ID.Mighty_Gorgon: 1028,
    ID.Wyvern: 1350,
    ID.Wyvern_Monarch: 1518,
    ID.Hydra: 4120,
    ID.Chaos_Hydra: 5931,
    ID.Pixie: 55,
    ID.Sprite: 95,
    ID.Air_Elemental: 356,
    ID.Storm_Elemental: 486,
    ID.Water_Elemental: 315,
    ID.Ice_Elemental: 380,
    ID.Fire_Elemental: 345,
    ID.Energy_Elemental: 470,
    ID.Earth_Elemental: 330,
    ID.Magma_Elemental: 490,
    ID.Psychic_Elemental: 1669,
    ID.Magic_Elemental: 2012,
    ID.Firebird: 4336,
    ID.Phoenix: 6721,
    ID.Nymph: 57,
    ID.Oceanid: 75,
    ID.Crew_Mate: 155,
    ID.Seaman: 174,
    ID.Pirate: 312,
    ID.Corsair: 407,
    ID.Sea_Dog: 602,
    ID.Stormbird: 502,
    ID.Ayssid: 645,
    ID.Sea_Witch: 790,
    ID.Sorceress: 852,
    ID.Nix: 1415,
    ID.Nix_Warrior: 2116,
    ID.Sea_Serpent: 3953,
    ID.Haspid: 7220,
    ID.Halfling: 75,
    ID.Halfling_Grenadier: 95,
    ID.Mechanic: 186,
    ID.Engineer: 278,
    ID.Armadillo: 198,
    ID.Bellwether_Armadillo: 256,
    ID.Automaton: 669,
    ID.Sentinel_Automaton: 947,
    ID.Sandworm: 991,
    ID.Olgoi_Khorkhoi: 1220,
    ID.Gunslinger: 1351,
    ID.Bounty_Hunter: 1454,
    ID.Couatl: 3574,
    ID.Crimson_Couatl: 5341,
    ID.Dreadnought: 3879,
    ID.Juggernaut: 6433,
    ID.Kobold: 54,
    ID.Kobold_Foreman: 84,
    ID.Mountain_Ram: 228,
    ID.Argali: 250,
    ID.Snow_Elf: 370,
    ID.Steel_Elf: 526,
    ID.Yeti: 504,
    ID.Yeti_Runemaster: 751,
    ID.Shaman: 685,
    ID.Great_Shaman: 818,
    ID.Mammoth: 1359,
    ID.War_Mammoth: 1601,
    ID.Jotunn: 4180,
    ID.Jotunn_Warlord: 6694,
    ID.Peasant: 15,
    ID.Boar: 145,
    ID.Rogue: 135,
    ID.Leprechaun: 208,
    ID.Mummy: 270,
    ID.Nomad: 345,
    ID.Sharpshooter: 585,
    ID.Satyr: 518,
    ID.Steel_Golem: 597,
    ID.Troll: 1024,
    ID.Gold_Golem: 600,
    ID.Fangarm: 929,
    ID.Diamond_Golem: 775,
    ID.Enchanter: 1210,
    ID.Faerie_Dragon: 30501,
    ID.Rust_Dragon: 26433,
    ID.Crystal_Dragon: 39338,
    ID.Azure_Dragon: 78845,
}
