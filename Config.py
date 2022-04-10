
screen_width, screen_height = 1280,720

game_x, game_y = 420,60
game_width, game_height = 800,600

game_left = game_x
game_right = game_x + game_width
game_top = game_y
game_bottom = game_y + game_height

frame_rate = 60
frame_time = 1/frame_rate
frame_time_millis = int(frame_time * 1000)


debug_player_invincible = False
debug_player_hitbox_show = False

debug_ray_show = True
debug_ray_tip_show = False
debug_ray_distance_show = True