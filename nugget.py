from gfx_pack import SWITCH_B, SWITCH_C, SWITCH_D, SWITCH_E

class Scene():
    def pressed_button(self, button, display):
        result = False
        if button == SWITCH_B:
            result = self.pressed_b()
        elif button == SWITCH_C:
            result = self.pressed_c()
        elif button == SWITCH_D:
            result = self.pressed_d()
        elif button == SWITCH_E:
            result = self.pressed_e()
        self.draw(display) if not result else self.end_screen(display)
        return result

    def pressed_b(self):
        return False

    def pressed_c(self):
        return False

    def pressed_d(self):
        return False

    def pressed_e(self):
        return False

    def draw(self, display):
        pass

    def end_screen(self, display):
        pass
