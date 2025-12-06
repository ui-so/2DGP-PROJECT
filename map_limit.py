import play_mode

size = 50

MAP_LIMITS = {
    'spawn_1': (1925, 890, 300, 230, 1225, 840, 1725, 1010),
    'farm': (780, 935, 515, 345, 1225, 840, 1725, 1010),
    'spawn_2': (1925, 890, 300, 230, 2100, 840, 3025, 940),
    'prairie_1': (3670, 860, 890, 520, 2100, 840, 3025, 940),
    'prairie_2': (3670, 860, 890, 520, 3610, 1260, 3710, 2300),
    'lava_1': (3650, 2570, 900, 500, 3610, 1260, 3710, 2300),
    'lava_2': (3650, 2570, 900, 500, 2100, 2450, 3025, 2550),
    'lava_3': (3650, 2570, 900, 500, 3500, 2960, 3600, 3650),
    'ice_1': (1200, 2500, 900, 520, 2100, 2450, 3025, 2550),
    'cave_1': (3500, 4080, 1000, 500, 3500, 2960, 3600, 3650),
    'cave_2': (3500, 4080, 1000, 500, 1800, 3950, 3025, 4050),
    'end_1': (1100, 4050, 800, 420, 1800, 3950, 3025, 4050),
}

MAP_OBSTACLES = {
    'spawn_1': [(1710, 1000, 2110, 1130)],   # 1910, 1050 기준 +- 100, 80
    'spawn_2': [(1710, 1000, 2110, 1130)],
    'farm': [(835-30, 960+40, 1130+30, 1150+50),(385-30, 960+40, 680+30, 1150+50),
             (791-30, 680+40, 1086+30, 870+50),(341-30, 680+40, 636+30, 870+50)],
}


def check_map_transition(current_map, x, y):
    next_map = None
    next_island = None

    if current_map == 'spawn_1':
        if x < 1525: return 'farm', None
        if play_mode.BRIDGE[0] == 1:
            if x > 2000: return 'spawn_2', None

    elif current_map == 'spawn_2':
        if x < 1950:
            return 'spawn_1', None
        elif x > 2500:
            return 'prairie_1', 'prairie'

    elif current_map == 'farm':
        if x > 1525: return 'spawn_1', 'spawn'

    elif current_map == 'prairie_1':
        if play_mode.BRIDGE[1] == 1:
            if y > 1100: return 'prairie_2', None
        elif x < 2500:
            return 'spawn_2', None

    elif current_map == 'prairie_2':
        if y < 1100:
            return 'prairie_1', None
        elif y > 2000:
            return 'lava_1', 'lava'

    elif current_map == 'lava_1':
        if y < 1500:
            return 'prairie_2', 'prairie'
        if play_mode.BRIDGE[2] == 1:
            if x < 3000:
                return 'lava_2', None
        if play_mode.BRIDGE[3] == 1:
            if y > 2700:
                return 'lava_3', None

    elif current_map == 'lava_2':
        if x > 3000:
            return 'lava_1', None
        elif x < 2300:
            return 'ice_1', 'ice'

    elif current_map == 'lava_3':
        if y < 2500:
            return 'lava_1', None
        elif y > 3200:
            return 'cave_1', 'cave'

    elif current_map == 'ice_1':
        if x > 2300: return 'lava_2', 'lava'

    elif current_map == 'cave_1':
        if y < 3500:
            return 'lava_3', 'lava'
        if play_mode.BRIDGE[4] == 1:
            if x < 2600:
                return 'cave_2', None

    elif current_map == 'cave_2':
        if x < 2300:
            return 'end_1', 'end'
        elif y < 3800:
            return 'cave_1', None

    elif current_map == 'end_1':
        if x > 2300: return 'cave_1', 'cave'

    return None, None