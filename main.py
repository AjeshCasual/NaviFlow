import pyray as rl
rl.init_window(660, 450, "NaviFlow")

rl.set_target_fps(60)
while not rl.window_should_close():
    rl.begin_drawing()
    rl.clear_background(rl.WHITE)

    rl.draw_rectangle_pro(rl.Rectangle(360,240,300,200),rl.Vector2(0,0),90,rl.RED)
    rl.draw_rectangle_lines_ex(rl.Rectangle(360,240,300,200),10,rl.GREEN)
   
    rl.end_drawing()
rl.close_window()