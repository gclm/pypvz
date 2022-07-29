import pygame as pg
from .. import tool
from .. import constants as c

class Screen(tool.State):
    def __init__(self):
        tool.State.__init__(self)
        self.end_time = 3000

    def startup(self, current_time, persist):
        pass
    
    def getImageName(self):
        pass

    def set_next_state(self):
        pass

    def setupImage(self, name, frame_rect=(0, 0, 800, 600)):
        self.image = tool.get_image(tool.GFX[name], *frame_rect)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self, surface, current_time, mouse_pos, mouse_click):
        if (current_time - self.start_time) < self.end_time:
            surface.fill(c.WHITE)
            surface.blit(self.image, self.rect)
        else:
            self.done = True

class GameVictoryScreen(Screen):
    def __init__(self):
        Screen.__init__(self)
    
    def getImageName(self):
        return c.GAME_VICTORY_IMAGE
    
    def set_next_state(self):
        return c.LEVEL
    
    def startup(self, current_time, persist):
        self.start_time = current_time
        self.next = c.LEVEL
        self.persist = persist
        self.game_info = persist
        name = self.getImageName()
        self.setupImage(name)
        self.next = self.set_next_state()
        pg.display.set_caption("pypvz: 战斗胜利！")

class GameLoseScreen(Screen):
    def __init__(self):
        Screen.__init__(self)
    
    def getImageName(self):
        return c.GAME_LOSE_IMAGE
    
    def set_next_state(self):
        return c.LEVEL
    
    def startup(self, current_time, persist):
        self.start_time = current_time
        self.next = c.LEVEL
        self.persist = persist
        self.game_info = persist
        name = self.getImageName()
        self.setupImage(name, (-15, 0, 800, 600))
        self.next = self.set_next_state()
        pg.display.set_caption("pypvz: 战斗失败！")

class AwardScreen(tool.State):
    def __init__(self):
        tool.State.__init__(self)

    def setupImage(self):
        # 主体
        frame_rect = (0, 0, 800, 600)
        self.image = tool.get_image(tool.GFX[c.AWARD_SCREEN_IMAGE], *frame_rect)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

        # 文字
        # 标题处文字
        font = pg.font.Font(c.FONT_PATH, 37)
        title_text = font.render("您得到了新的战利品！", True, c.PARCHMENT_YELLOW)
        title_text_rect = title_text.get_rect()
        title_text_rect.x = 220
        title_text_rect.y = 23
        self.image.blit(title_text, title_text_rect)
        
        # 按钮
        frame_rect = (0, 0, 111, 26)
        if self.show_only_one_option:
            ## 主菜单按钮
            self.main_menu_button_image = tool.get_image_menu(tool.GFX[c.UNIVERSAL_BUTTON], *frame_rect)
            self.main_menu_button_image_rect = self.main_menu_button_image.get_rect()
            self.main_menu_button_image_rect.x = 343
            self.main_menu_button_image_rect.y = 520
            ### 主菜单按钮上的文字
            font = pg.font.Font(c.FONT_PATH, 18)
            main_menu_text = font.render("主菜单", True, c.NAVYBLUE)
            main_menu_text_rect = main_menu_text.get_rect()
            main_menu_text_rect.x = 29
            self.main_menu_button_image.blit(main_menu_text, main_menu_text_rect)
            self.image.blit(self.main_menu_button_image, self.main_menu_button_image_rect)
        else:
            ## 继续按钮
            self.next_button_image = tool.get_image_menu(tool.GFX[c.UNIVERSAL_BUTTON], *frame_rect)
            self.next_button_image_rect = self.next_button_image.get_rect()
            self.next_button_image_rect.x = 70
            ### 继续按钮上的文字
            font = pg.font.Font(c.FONT_PATH, 18)
            next_text = font.render("继续", True, c.NAVYBLUE)
            next_text_rect = next_text.get_rect()
            next_text_rect.x = 37
            ## 主菜单按钮
            self.main_menu_button_image = tool.get_image_menu(tool.GFX[c.UNIVERSAL_BUTTON], *frame_rect)
            self.main_menu_button_image_rect = self.main_menu_button_image.get_rect()
            self.main_menu_button_image_rect.x = 620
            self.next_button_image_rect.y = self.main_menu_button_image_rect.y = 540
            ### 主菜单按钮上的文字
            main_menu_text = font.render("主菜单", True, c.NAVYBLUE)
            main_menu_text_rect = main_menu_text.get_rect()
            main_menu_text_rect.x = 29
            self.next_button_image.blit(next_text, next_text_rect)
            self.main_menu_button_image.blit(main_menu_text, main_menu_text_rect)
            self.image.blit(self.next_button_image, self.next_button_image_rect)
            self.image.blit(self.main_menu_button_image, self.main_menu_button_image_rect)

        # 显示向日葵奖杯的情况
        if self.show_only_one_option:
            if self.game_info[c.LITTLEGAME_COMPLETIONS]:
                frame_rect = (157, 0, 157, 269)
            else:
                frame_rect = (0, 0, 157, 269)
            sunflower_trophy_image = tool.get_image_menu(tool.GFX[c.TROPHY_SUNFLOWER], *frame_rect, scale=0.7)
            sunflower_trophy_rect = sunflower_trophy_image.get_rect()
            sunflower_trophy_rect.x = 348
            sunflower_trophy_rect.y = 110
            self.image.blit(sunflower_trophy_image, sunflower_trophy_rect)

    def startup(self, current_time, persist):
        self.start_time = current_time
        self.persist = persist
        self.game_info = persist
        if (c.PASSED_ALL in self.game_info) and (not self.game_info[c.PASSED_ALL]):
            self.show_only_one_option = False
        else:
            self.show_only_one_option = True
        self.setupImage()
        pg.display.set_caption("pypvz: 您获得了新的战利品！")

    def update(self, surface, current_time, mouse_pos, mouse_click):
        surface.fill(c.WHITE)
        surface.blit(self.image, self.rect)
        if mouse_pos:
            # 检查主菜单点击
            if self.inArea(self.main_menu_button_image_rect, *mouse_pos):
                self.next = c.MAIN_MENU
                self.done = True
            elif not self.show_only_one_option:
                if self.inArea(self.next_button_image_rect, *mouse_pos):
                    self.next = c.LEVEL
                    self.done = True

    def inArea(self, rect, x, y):
        if (x >= rect.x and x <= rect.right and
            y >= rect.y and y <= rect.bottom):
            return True
        else:
            return False
