#!/usr/bin/env python
import logging
import traceback
import os
import pygame as pg
from logging.handlers import RotatingFileHandler
# 由于在后续本地模块中存在对pygame的调用，因此必须在这里完成pygame的初始化
pg.init()

from source import tool
from source import constants as c
from source.state import mainmenu, screen, level

if __name__=="__main__":
    # 日志设置
    if not os.path.exists(os.path.dirname(c.USERLOG_PATH)):
        os.makedirs(os.path.dirname(c.USERLOG_PATH))
    logger = logging.getLogger()
    formatter = logging.Formatter("%(asctime)s: %(message)s")
    fileHandler = RotatingFileHandler(c.USERLOG_PATH, "a", 1024*1024, 0, "utf-8")
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)

    try:
        # 控制状态机运行
        game = tool.Control()
        state_dict = {  c.MAIN_MENU:    mainmenu.Menu(),
                        c.GAME_VICTORY: screen.GameVictoryScreen(),
                        c.GAME_LOSE:    screen.GameLoseScreen(),
                        c.LEVEL:        level.Level()
                        }
        game.setup_states(state_dict, c.MAIN_MENU)
        game.run()
    except:
        print() # 将日志输出与上文内容分隔开，增加可读性
        logger.error(f"\n{traceback.format_exc()}") 
