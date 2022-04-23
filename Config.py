import time

screen_width, screen_height = 1280,720

game_x, game_y = 420,60
game_width, game_height = 800,600

game_left = game_x
game_right = game_x + game_width
game_top = game_y
game_bottom = game_y + game_height

game_draw_bg = True

asteriod_spawnrate = 1

player_disableshooting = True

genetic_simulationtime = 60
genetic_agentpergeneration = 100

score_per_second_surving = 100
score_per_asteriod = 0.0
score_per_distance_traveled = 0.0

random_fixedseedeverygeneration = False
randomseed = int(time.time()) 
randomseed = 1

speedmultiplier = 4
frame_rate = 60
frame_time = 1/frame_rate
frame_time_millis = int(frame_time * 1000)

infopanel_left = 60
infopanel_right = game_x - 20
infopanel_top = game_top
infopanel_bottom = game_bottom

infopanel_width = infopanel_right - infopanel_left
infopanel_height = game_height

##### DEBUG

debug_player_neuralcontrol = True
debug_player_manualcontrol = True

debug_player_invincible = False
debug_player_hitbox_show = False

debug_ray_show = True
debug_ray_tip_show = True
debug_ray_distance_show = True