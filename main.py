from time import sleep
from gfx_pack import GfxPack, SWITCH_A, SWITCH_B, SWITCH_C, SWITCH_D, SWITCH_E
from drawing_helpers import clear
from ttt import TicTacToe

# Initialize display
gp = GfxPack()
gp.set_backlight(0, 0, 0, 128)
display = gp.display

scene_stack = [TicTacToe()]
new_scene = True

while True:
    # TODO: Will likely need to modify the interface to allow for parametrically adding scenes
    if new_scene:
        if len(scene_stack) == 0:
            scene_stack.append(TicTacToe())
        scene_stack[-1].draw(display)
        new_scene = False
    elif gp.switch_pressed(SWITCH_A):
        # TODO: Implement escape/scene stack pop functionality
        continue
    else:
        for switch in (SWITCH_B, SWITCH_C, SWITCH_D, SWITCH_E):
            if gp.switch_pressed(switch):
                if scene_stack[-1].pressed_button(switch, display):
                    scene_stack.pop()
                    new_scene = True
                break
    sleep(0.05)
                