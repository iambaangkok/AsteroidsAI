
screen_width, screen_height = 1280,720

game_x, game_y = 420,60
game_width, game_height = 800,600

game_left = game_x
game_right = game_x + game_width
game_top = game_y
game_bottom = game_y + game_height

game_draw_bg = False

genetic_agentpergeneration = 5

infopanel_left = 60
infopanel_right = game_x - 20
infopanel_top = game_top
infopanel_bottom = game_bottom

infopanel_width = infopanel_right - infopanel_left
infopanel_height = game_height

speedmultiplier = 1
frame_rate = 60
frame_time = 1/frame_rate
frame_time_millis = int(frame_time * 1000)

##### DEBUG

debug_player_neuralcontrol = True

debug_player_manualcontrol = False
debug_player_invincible = False
debug_player_hitbox_show = False

debug_ray_show = True
debug_ray_tip_show = True
debug_ray_distance_show = True