from enum import IntEnum

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
    NONE = 65535 # 2 bytes max



    Pikeman              =   0
    Halberdier           =   1
    Archer               =   2
    Marksman             =   3
    Griffin              =   4
    Royal_Griffin        =   5
    Swordsman            =   6
    Crusader             =   7
    Monk                 =   8
    Zealot               =   9
    Cavalier             =  10
    Champion             =  11
    Angel                =  12
    Archangel            =  13
    Centaur              =  14
    Centaur_Captain      =  15
    Dwarf                =  16
    Battle_Dwarf         =  17
    Wood_Elf             =  18
    Grand_Elf            =  19
    Pegasus              =  20
    Silver_Pegasus       =  21
    Dendroid_Guard       =  22
    Dendroid_Soldier     =  23
    Unicorn              =  24
    War_Unicorn          =  25
    Green_Dragon         =  26
    Gold_Dragon          =  27
    Gremlin              =  28
    Master_Gremlin       =  29
    Stone_Gargoyle       =  30
    Obsidian_Gargoyle    =  31
    Stone_Golem          =  32
    Iron_Golem           =  33
    Mage                 =  34
    Arch_Mage            =  35
    Genie                =  36
    Master_Genie         =  37
    Naga                 =  38
    Naga_Queen           =  39
    Giant                =  40
    Titan                =  41
    Imp                  =  42
    Familiar             =  43
    Gog                  =  44
    Magog                =  45
    Hell_Hound           =  46
    Cerberus             =  47
    Demon                =  48
    Horned_Demon         =  49
    Pit_Fiend            =  50
    Pit_Lord             =  51
    Efreeti              =  52
    Efreet_Sultan        =  53
    Devil                =  54
    Arch_Devil           =  55
    Skeleton             =  56
    Skeleton_Warrior     =  57
    Walking_Dead         =  58
    Zombie               =  59
    Wight                =  60
    Wraith               =  61
    Vampire              =  62
    Vampire_Lord         =  63
    Lich                 =  64
    Power_Lich           =  65
    Black_Knight         =  66
    Dread_Knight         =  67
    Bone_Dragon          =  68
    Ghost_Dragon         =  69
    Troglodyte           =  70
    Infernal_Troglodyte  =  71
    Harpy                =  72
    Harpy_Hag            =  73
    Beholder             =  74
    Evil_Eye             =  75
    Medusa               =  76
    Medusa_Queen         =  77
    Minotaur             =  78
    Minotaur_King        =  79
    Manticore            =  80
    Scorpicore           =  81
    Red_Dragon           =  82
    Black_Dragon         =  83
    Goblin               =  84
    Hobgoblin            =  85
    Wolf_Rider           =  86
    Wolf_Raider          =  87
    Orc                  =  88
    Orc_Chieftain        =  89
    Ogre                 =  90
    Ogre_Mage            =  91
    Roc                  =  92
    Thunderbird          =  93
    Cyclops              =  94
    Cyclops_King         =  95
    Behemoth             =  96
    Ancient_Behemoth     =  97
    Gnoll                =  98
    Gnoll_Marauder       =  99
    Lizardman            = 100
    Lizard_Warrior       = 101
    Gorgon               = 102
    Mighty_Gorgon        = 103
    Serpent_Fly          = 104
    Dragon_Fly           = 105
    Basilisk             = 106
    Greater_Basilisk     = 107
    Wyvern               = 108
    Wyvern_Monarch       = 109
    Hydra                = 110
    Chaos_Hydra          = 111
    Air_Elemental        = 112
    Earth_Elemental      = 113
    Fire_Elemental       = 114
    Water_Elemental      = 115
    Gold_Golem           = 116
    Diamond_Golem        = 117
    Pixie                = 118
    Sprite               = 119
    Psychic_Elemental    = 120
    Magic_Elemental      = 121
    NOT_USED_1           = 122
    Ice_Elemental        = 123
    NOT_USED_2           = 124
    Magma_Elemental      = 125
    NOT_USED_3           = 126
    Storm_Elemental      = 127
    NOT_USED_4           = 128
    Energy_Elemental     = 129
    Firebird             = 130
    Phoenix              = 131
    Azure_Dragon         = 132
    Crystal_Dragon       = 133
    Faerie_Dragon        = 134
    Rust_Dragon          = 135
    Enchanter            = 136
    Sharpshooter         = 137
    Halfling             = 138
    Peasant              = 139
    Boar                 = 140
    Mummy                = 141
    Nomad                = 142
    Rogue                = 143
    Troll                = 144
    Catapult             = 145
    Ballista             = 146
    First_Aid_Tent       = 147
    Ammo_Cart            = 148
    Arrow_Tower          = 149
    Cannon               = 150
    Sea_Dog              = 151
    Electric_Tower       = 152
    Nymph                = 153
    Oceanid              = 154
    Crew_Mate            = 155
    Seaman               = 156
    Pirate               = 157
    Corsair              = 158
    Stormbird            = 159
    Ayssid               = 160
    Sea_Witch            = 161
    Sorceress            = 162
    Nix                  = 163
    Nix_Warrior          = 164
    Sea_Serpent          = 165
    Haspid               = 166
    Satyr                = 167
    Fangarm              = 168
    Leprechaun           = 169
    Steel_Golem          = 170
    Halfling_Grenadier   = 171
    Mechanic             = 172
    Engineer             = 173
    Armadillo            = 174
    Bellwether_Armadillo = 175
    Automaton            = 176
    Sentinel_Automaton   = 177
    Sandworm             = 178
    Olgoi_Khorkhoi       = 179
    Gunslinger           = 180
    Bounty_Hunter        = 181
    Couatl               = 182
    Crimson_Couatl       = 183
    Dreadnought          = 184
    Juggernaut           = 185

NAME = [
    "Pikemen" , "Halberdiers"   , "Archers"  , "Marksmen" ,
    "Griffins", "Royal Griffins", "Swordsmen", "Crusaders",
    "Monks"   , "Zealots"       , "Cavaliers", "Champions",
    "Angels"  , "Archangels"    ,

    "Centaurs"       , "Centaur Captains" , "Dwarves" , "Battle Dwarves",
    "Wood Elves"     , "Grand Elves"      , "Pegasi"  , "Silver Pegasi" ,
    "Dendroid Guards", "Dendroid Soldiers", "Unicorns", "War Unicorns"  ,
    "Green Dragons"  , "Gold Dragons"     ,

    "Gremlins"    , "Master Gremlins", "Stone Gargoyles", "Obsidian Gargoyles",
    "Stone Golems", "Iron Golems"    , "Magi"           , "Arch Magi"         ,
    "Genies"      , "Master Genies"  , "Nagas"          , "Naga Queens"       ,
    "Giants"      , "Titans"         ,

    "Imps"       , "Familiars"  , "Gogs"  , "Magogs"        ,
    "Hell Hounds", "Cerberi"    , "Demons", "Horned Demons" ,
    "Pit Fiends" , "Pit Lords"  , "Efreet", "Efreet Sultans",
    "Devils"     , "Arch Devils",

    "Skeletons"   , "Skeleton Warriors", "Walking Dead" , "Zombies"      ,
    "Wights"      , "Wraiths"          , "Vampires"     , "Vampire Lords",
    "Liches"      , "Power Liches"     , "Black Knights", "Dread Knights",
    "Bone Dragons", "Ghost Dragons"    ,

    "Troglodytes", "Infernal Troglodytes", "Harpies"   , "Harpy Hags"   ,
    "Beholders"  , "Evil Eyes"           , "Medusas"   , "Medusa Queens",
    "Minotaurs"  , "Minotaur Kings"      , "Manticores", "Scorpicores"  ,
    "Red Dragons", "Black Dragons"       ,

    "Goblins"  , "Hobgoblins"       , "Wolf Riders", "Wolf Raiders" ,
    "Orcs"     , "Orc Chieftains"   , "Ogres"      , "Ogre Magi"    ,
    "Rocs"     , "Thunderbirds"     , "Cyclopes"   , "Cyclops Kings",
    "Behemoths", "Ancient Behemoths",

    "Gnolls"   , "Gnoll Marauders"  , "Lizardmen"    , "Lizard Warriors",
    "Gorgons"  , "Mighty Gorgons"   , "Serpent Flies", "Dragon Flies"   ,
    "Basilisks", "Greater Basilisks", "Wyverns"      , "Wyvern Monarchs",
    "Hydras"   , "Chaos Hydras"     ,

    "Air Elementals" , "Earth Elementals",
    "Fire Elementals", "Water Elementals",
    "Gold Golems"    , "Diamond Golems"  ,

    "Pixies"    , "Sprites"         , "Psychic Elementals", "Magic Elementals" ,
    "NOT USED 1", "Ice Elementals"  , "NOT USED 2"        , "Magma Elementals" ,
    "NOT USED 3", "Storm Elementals", "NOT USED 4"        , "Energy Elementals",
    "Firebirds" , "Phoenixes"       ,

    "Azure Dragons", "Crystal Dragons", "Faerie Dragons", "Rust Dragons"   ,
    "Enchanters"   , "Sharpshooters"  , "Halflings"     , "Peasants"       ,
    "Boars"        , "Mummies"        , "Nomads"        , "Rogues"         ,
    "Trolls"       ,

    "Catapults" , "Ballistas"   , "First Aid Tents",
    "Ammo Carts", "Arrow Towers", "Cannons"        ,

    "Sea Dogs"    , "Electric Towers",
    "Nymphs"      , "Oceanids"       , "Crew Mates", "Seamen"      ,
    "Pirates"     , "Corsairs"       , "Stormbirds", "Ayssids"     ,
    "Sea Witches" , "Sorceresses"    , "Nixes"     , "Nix Warriors",
    "Sea Serpents", "Haspids"        ,

    "Satyrs", "Fangarms", "Leprechauns", "Steel Golems",

    "Halfling Grenadiers"  , "Mechanics"   , "Engineers"          , "Armadillos",
    "Bellwether Armadillos", "Automatons"  , "Sentinel Automatons", "Sandworms" ,
    "Olgoi-Khorkhoi"       , "Gunslingers" , "Bounty Hunters"     , "Couatls"   ,
    "Crimson Couatls"      , "Dreadnoughts", "Juggernauts"
]

AI_VALUE = [
       80, # Pikeman
      115, # Halberdier
      126, # Archer
      184, # Marksman
      351, # Griffin
      448, # Royal_Griffin
      445, # Swordsman
      588, # Crusader
      582, # Monk
      750, # Zealot
     1946, # Cavalier
     2100, # Champion
     5019, # Angel
     8776, # Archangel
      100, # Centaur
      138, # Centaur_Captain
      138, # Dwarf
      209, # Battle_Dwarf
      234, # Wood_Elf
      331, # Grand_Elf
      518, # Pegasus
      532, # Silver_Pegasus
      517, # Dendroid_Guard
      803, # Dendroid_Soldier
     1806, # Unicorn
     2030, # War_Unicorn
     4872, # Green_Dragon
     8613, # Gold_Dragon
       44, # Gremlin
       66, # Master_Gremlin
      165, # Stone_Gargoyle
      201, # Obsidian_Gargoyle
      250, # Stone_Golem
      412, # Iron_Golem
      570, # Mage
      680, # Arch_Mage
      884, # Genie
      942, # Master_Genie
     2016, # Naga
     2840, # Naga_Queen
     3718, # Giant
     7500, # Titan
       50, # Imp
       60, # Familiar
      159, # Gog
      240, # Magog
      357, # Hell_Hound
      392, # Cerberus
      445, # Demon
      480, # Horned_Demon
      765, # Pit_Fiend
     1224, # Pit_Lord
     1670, # Efreeti
     2343, # Efreet_Sultan
     5101, # Devil
     7115, # Arch_Devil
       60, # Skeleton
       85, # Skeleton_Warrior
       98, # Walking_Dead
      128, # Zombie
      252, # Wight
      315, # Wraith
      555, # Vampire
      783, # Vampire_Lord
      848, # Lich
     1079, # Power_Lich
     2087, # Black_Knight
     2382, # Dread_Knight
     3388, # Bone_Dragon
     4696, # Ghost_Dragon
       59, # Troglodyte
       84, # Infernal_Troglodyte
      154, # Harpy
      238, # Harpy_Hag
      336, # Beholder
      367, # Evil_Eye
      517, # Medusa
      577, # Medusa_Queen
      835, # Minotaur
     1068, # Minotaur_King
     1547, # Manticore
     1589, # Scorpicore
     4702, # Red_Dragon
     8721, # Black_Dragon
       60, # Goblin
       78, # Hobgoblin
      130, # Wolf_Rider
      203, # Wolf_Raider
      192, # Orc
      240, # Orc_Chieftain
      416, # Ogre
      672, # Ogre_Mage
     1027, # Roc
     1106, # Thunderbird
     1266, # Cyclops
     1443, # Cyclops_King
     3162, # Behemoth
     6188, # Ancient_Behemoth
       56, # Gnoll
       90, # Gnoll_Marauder
      126, # Lizardman
      156, # Lizard_Warrior
      890, # Gorgon
     1028, # Mighty_Gorgon
      268, # Serpent_Fly
      312, # Dragon_Fly
      552, # Basilisk
      714, # Greater_Basilisk
     1350, # Wyvern
     1518, # Wyvern_Monarch
     4120, # Hydra
     5931, # Chaos_Hydra
      356, # Air_Elemental
      330, # Earth_Elemental
      345, # Fire_Elemental
      315, # Water_Elemental
      600, # Gold_Golem
      775, # Diamond_Golem
       55, # Pixie
       95, # Sprite
     1669, # Psychic_Elemental
     2012, # Magic_Elemental
        0, # NOT_USED_1
      380, # Ice_Elemental
        0, # NOT_USED_2
      490, # Magma_Elemental
        0, # NOT_USED_3
      486, # Storm_Elemental
        0, # NOT_USED_4
      470, # Energy_Elemental
     4336, # Firebird
     6721, # Phoenix
    78845, # Azure_Dragon
    39338, # Crystal_Dragon
    30501, # Faerie_Dragon
    26433, # Rust_Dragon
     1210, # Enchanter
      585, # Sharpshooter
       75, # Halfling
       15, # Peasant
      145, # Boar
      270, # Mummy
      345, # Nomad
      135, # Rogue
     1024, # Troll
      500, # Catapult
      600, # Ballista
      300, # First_Aid_Tent
      400, # Ammo_Cart
      400, # Arrow_Tower
      875, # Cannon
      602, # Sea_Dog
        0, # Electric Tower
       57, # Nymph
       75, # Oceanid
      155, # Crew_Mate
      174, # Seaman
      312, # Pirate
      407, # Corsair
      502, # Stormbird
      645, # Ayssid
      790, # Sea_Witch
      852, # Sorceress
     1415, # Nix
     2116, # Nix_Warrior
     3953, # Sea_Serpent
     7220, # Haspid
      518, # Satyr
      929, # Fangarm
      208, # Leprechaun
      597, # Steel_Golem
       95, # Halfling Grenadier
      186, # Mechanic
      278, # Engineer
      198, # Armadillo
      256, # Bellwether Armadillo
      669, # Automaton
      947, # Sentinel Automaton
      991, # Sandworm
     1220, # Olgoi-Khorkhoi
     1351, # Gunslinger
     1454, # Bounty Hunter
     3574, # Couatl
     5341, # Crimson Couatl
     3879, # Dreadnought
     6433  # Juggernaut
]
