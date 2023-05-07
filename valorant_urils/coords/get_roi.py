from dataclasses import dataclass
@dataclass
class Area:
    name:str
    top_x:int
    top_y:int
    bottom_x:int
    bottom_y:int

minimap = Area('minimap',15,40,435,460)
left_team = Area('left_team',440,0,870,100)
right_team = Area('right_team',1050,0,1480,100)
timer = Area('timer',870,0,1050,100)
kill_log = Area('kill_log',1490,60,1920,300)
hp = Area('hp',520,980,685,1080)
skill = Area('skill',745,980,1175,1080)
amo = Area('amo',1235,980,1400,1080)
center = ('center',960,540,125)

def get_roi(x, y):
    if ((x - center[1])**2 + (y - center[2])**2) <= center[3]**2:
        return center[0]
    elif left_team.top_x <= x <= left_team.bottom_x and left_team.top_y <= y <= left_team.bottom_y:
        return left_team.name
    elif right_team.top_x <= x <= right_team.bottom_x and right_team.top_y <= y <= right_team.bottom_y:
        return right_team.name
    elif timer.top_x <= x <= timer.bottom_x and timer.top_y <= y <= timer.bottom_y:
        return timer.name
    elif kill_log.top_x <= x <= kill_log.bottom_x and kill_log.top_y <= y <= kill_log.bottom_y:
        return kill_log.name
    elif hp.top_x <= x <= hp.bottom_x and hp.top_y <= y <= hp.bottom_y:
        return hp.name
    elif skill.top_x <= x <= skill.bottom_x and skill.top_y <= y <= skill.bottom_y:
        return skill.name
    elif amo.top_x <= x <= amo.bottom_x and amo.top_y <= y <= amo.bottom_y:
        return amo.name
    elif minimap.top_x <= x <= minimap.bottom_x and minimap.top_y <= y <= minimap.bottom_y:
        return minimap.name
    else:
        return 'other'
    
    