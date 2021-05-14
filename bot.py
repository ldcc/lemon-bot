import nonebot
from nonebot.adapters.cqhttp import Bot

nonebot.init()
driver = nonebot.get_driver()
driver.register_adapter('cqhttp', Bot)
nonebot.load_plugins("src/plugins")

if __name__ == '__main__':
    nonebot.run()
