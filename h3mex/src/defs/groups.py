from . import objects

##############################
# HEROES
##############################

HEROES = {
    objects.ID.Hero,
    objects.ID.Random_Hero,
    objects.ID.Prison,
    objects.ID.Hero_Placeholder,
}


##############################
# MONSTERS
##############################

RANDOM_MONSTERS_LEVEL = {
    objects.ID.Random_Monster_1,
    objects.ID.Random_Monster_2,
    objects.ID.Random_Monster_3,
    objects.ID.Random_Monster_4,
    objects.ID.Random_Monster_5,
    objects.ID.Random_Monster_6,
    objects.ID.Random_Monster_7,
}
RANDOM_MONSTERS = {objects.ID.Random_Monster, *RANDOM_MONSTERS_LEVEL}
MONSTERS = {objects.ID.Monster, *RANDOM_MONSTERS}


##############################
# ARTIFACTS
##############################

RANDOM_ARTIFACTS = {
    objects.ID.Random_Artifact,
    objects.ID.Random_Treasure_Artifact,
    objects.ID.Random_Minor_Artifact,
    objects.ID.Random_Major_Artifact,
    objects.ID.Random_Relic,
}
ARTIFACTS = {objects.ID.Artifact, *RANDOM_ARTIFACTS}


##############################
# RESOURCES
##############################

RESOURCES = {objects.ID.Resource, objects.ID.Random_Resource}


##############################
# COLLECTIBLES
##############################

COLLECTIBLES = {
    objects.ID.Campfire,
    objects.ID.Flotsam,
    objects.ID.HotA_Pickup,
    objects.ID.Ocean_Bottle,
    objects.ID.Pandoras_Box,
    objects.ID.Scholar,
    objects.ID.Sea_Chest,
    objects.ID.Shipwreck_Survivor,
    objects.ID.Spell_Scroll,
    objects.ID.Treasure_Chest,
}


##############################
# MAGICAL TERRAIN
##############################

MAGICAL_TERRAIN = {
    objects.ID.Cursed_Ground_RoE,
    objects.ID.Magic_Plains_RoE,
    objects.ID.HotA_Magical_Terrain,
    objects.ID.Clover_Field,
    objects.ID.Cursed_Ground,
    objects.ID.Evil_Fog,
    objects.ID.Favorable_Winds,
    objects.ID.Fiery_Fields,
    objects.ID.Holy_Ground,
    objects.ID.Lucid_Pools,
    objects.ID.Magic_Clouds,
    objects.ID.Magic_Plains,
    objects.ID.Rocklands,
}


##############################
# PASSABLE
##############################

# PASSABLE = {
#     *HEROES,
#     *MONSTERS,
#     *ARTIFACTS,
#     *RESOURCES,
#     *COLLECTIBLES,
#     *MAGICAL_TERRAIN,
#     objects.ID.Boat,
#     objects.ID.Event_Object,
#     objects.ID.Grail,
#     objects.ID.HotA_Decor_1,
#     objects.ID.HotA_Decor_2,
# }

# PASSABLE_HOTA_DECOR_1 = {
#     0,
# }

# PASSABLE_HOTA_DECOR_2 = {
#     0,
# }


##############################
# BARRIERS
##############################

BORDER = {
    objects.ID.Border_Gate,
    objects.ID.Border_Guard,
    objects.ID.Garrison,
    objects.ID.Garrison_Vertical,
    objects.ID.Quest_Guard,
}


##############################
# MONOLITHS/PORTALS
##############################

ONE_WAY_MONOLITHS = {
    objects.SubID.MonolithPortal.OneWay.Blue_Monolith,
    objects.SubID.MonolithPortal.OneWay.Pink_Monolith,
    objects.SubID.MonolithPortal.OneWay.Orange_Monolith,
    objects.SubID.MonolithPortal.OneWay.Yellow_Monolith,
    objects.SubID.MonolithPortal.OneWay.Turquoise_Monolith,
    objects.SubID.MonolithPortal.OneWay.Violet_Monolith,
    objects.SubID.MonolithPortal.OneWay.Chartreuse_Monolith,
    objects.SubID.MonolithPortal.OneWay.White_Monolith,
}

ONE_WAY_PORTALS = {
    objects.SubID.MonolithPortal.OneWay.Purple_Portal,
    objects.SubID.MonolithPortal.OneWay.Orange_Portal,
    objects.SubID.MonolithPortal.OneWay.Red_Portal,
    objects.SubID.MonolithPortal.OneWay.Cyan_Portal,
}

TWO_WAY_MONOLITHS = {
    objects.SubID.MonolithPortal.TwoWay.Green_Monolith,
    objects.SubID.MonolithPortal.TwoWay.Brown_Monolith,
    objects.SubID.MonolithPortal.TwoWay.Violet_Monolith,
    objects.SubID.MonolithPortal.TwoWay.Orange_Monolith,
    objects.SubID.MonolithPortal.TwoWay.Pink_Monolith,
    objects.SubID.MonolithPortal.TwoWay.Turquoise_Monolith,
    objects.SubID.MonolithPortal.TwoWay.Yellow_Monolith,
    objects.SubID.MonolithPortal.TwoWay.Black_Monolith,
    objects.SubID.MonolithPortal.TwoWay.Blue_Monolith,
    objects.SubID.MonolithPortal.TwoWay.Red_Monolith,
}
TWO_WAY_PORTALS = {
    objects.SubID.MonolithPortal.TwoWay.Green_Portal,
    objects.SubID.MonolithPortal.TwoWay.Yellow_Portal,
    objects.SubID.MonolithPortal.TwoWay.Red_Portal,
    objects.SubID.MonolithPortal.TwoWay.Cyan_Portal,
    objects.SubID.MonolithPortal.TwoWay.Chartreuse_Portal,
    objects.SubID.MonolithPortal.TwoWay.Turquoise_Portal,
    objects.SubID.MonolithPortal.TwoWay.Violet_Portal,
    objects.SubID.MonolithPortal.TwoWay.Orange_Portal,
    objects.SubID.MonolithPortal.TwoWay.Pink_Portal,
    objects.SubID.MonolithPortal.TwoWay.Blue_Portal,
}
TWO_WAY_SEA_PORTALS = {
    objects.SubID.MonolithPortal.TwoWay.White_SeaPortal,
    objects.SubID.MonolithPortal.TwoWay.Red_SeaPortal,
    objects.SubID.MonolithPortal.TwoWay.Blue_SeaPortal,
    objects.SubID.MonolithPortal.TwoWay.Chartreuse_SeaPortal,
    objects.SubID.MonolithPortal.TwoWay.Yellow_SeaPortal,
}


##############################
# BARRIERS
##############################

BORDER = {
    objects.ID.Border_Gate,
    objects.ID.Border_Guard,
    objects.ID.Garrison,
    objects.ID.Garrison_Vertical,
    objects.ID.Quest_Guard,
}


##############################
# TRADING POSTS
##############################

TRADING_POSTS = {
    objects.ID.Trading_Post,
    objects.ID.Trading_Post_Snow,
}


##############################
# DECOR
##############################

DECOR = {
    objects.ID.Brush,
    objects.ID.Bush,
    objects.ID.Cactus,
    objects.ID.Canyon,
    objects.ID.Crater,
    objects.ID.Dead_Vegetation,
    objects.ID.Flowers,
    objects.ID.Frozen_Lake,
    objects.ID.Hedge,
    objects.ID.Hill,
    objects.ID.Hole,
    objects.ID.Kelp,
    objects.ID.Lake,
    objects.ID.Lava_Flow,
    objects.ID.Lava_Lake,
    objects.ID.Mushrooms,
    objects.ID.Log,
    objects.ID.Mandrake,
    objects.ID.Moss,
    objects.ID.Mound,
    objects.ID.Mountain,
    objects.ID.Oak_Trees,
    objects.ID.Outcropping,
    objects.ID.Pine_Trees,
    objects.ID.Plant,
    objects.ID.HotA_Decor_1,
    objects.ID.HotA_Decor_2,
    objects.ID.River_Delta,
    objects.ID.Rock,
    objects.ID.Sand_Dune,
    objects.ID.Sand_Pit,
    objects.ID.Shrub,
    objects.ID.Skull,
    objects.ID.Stalagmite,
    objects.ID.Stump,
    objects.ID.Tar_Pit,
    objects.ID.Trees,
    objects.ID.Vine,
    objects.ID.Volcanic_Vent,
    objects.ID.Volcano,
    objects.ID.Willow_Trees,
    objects.ID.Yucca_Trees,
    objects.ID.Reef,
    objects.ID.Brush_2,
    objects.ID.Bush_2,
    objects.ID.Cactus_2,
    objects.ID.Canyon_2,
    objects.ID.Crater_2,
    objects.ID.Dead_Vegetation_2,
    objects.ID.Flowers_2,
    objects.ID.Frozen_Lake_2,
    objects.ID.Hedge_2,
    objects.ID.Hill_2,
    objects.ID.Hole_2,
    objects.ID.Kelp_2,
    objects.ID.Lake_2,
    objects.ID.Lava_Flow_2,
    objects.ID.Lava_Lake_2,
    objects.ID.Mushrooms_2,
    objects.ID.Log_2,
    objects.ID.Mandrake_2,
    objects.ID.Moss_2,
    objects.ID.Mound_2,
    objects.ID.Mountain_2,
    objects.ID.Oak_Trees_2,
    objects.ID.Outcropping_2,
    objects.ID.Pine_Trees_2,
    objects.ID.Plant_2,
    objects.ID.River_Delta_2,
    objects.ID.Rock_2,
    objects.ID.Sand_Dune_2,
    objects.ID.Sand_Pit_2,
    objects.ID.Shrub_2,
    objects.ID.Skull_2,
    objects.ID.Stalagmite_2,
    objects.ID.Stump_2,
    objects.ID.Tar_Pit_2,
    objects.ID.Trees_2,
    objects.ID.Vine_2,
    objects.ID.Volcanic_Vent_2,
    objects.ID.Volcano_2,
    objects.ID.Willow_Trees_2,
    objects.ID.Yucca_Trees_2,
    objects.ID.Reef_2,
    objects.ID.Desert_Hills,
    objects.ID.Dirt_Hills,
    objects.ID.Grass_Hills,
    objects.ID.Rough_Hills,
    objects.ID.Subterranean_Rocks,
    objects.ID.Swamp_Foliage,
}
