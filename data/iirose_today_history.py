import requests

from loguru import logger
from API.api_message import at_user
from API.api_iirose import APIIirose  # 大部分接口都在这里
from globals.globals import GlobalVal  # 一些全局变量 now_room_id 是机器人当前所在的房间标识，websocket是ws链接，请勿更改其他参数防止出bug，也不要去监听ws，websockets库只允许一个接收流
from API.api_get_config import get_master_id  # 用于获取配置文件中主人的唯一标识
from API.decorator.command import on_command, MessageType  # 注册指令装饰器和消息类型Enmu

API = APIIirose()  # 吧class定义到变量就不会要求输入self了（虽然我都带了装饰器没有要self的 直接用APIIirose也不是不可以 习惯了

historyapi = "https://tools.mgtv100.com/external/v1/today_history"
newline = "\n"

@on_command('>历史上的今天', False, command_type=[MessageType.room_chat, MessageType.private_chat])  # command_type 参数可让本指令在哪些地方生效，发送弹幕需验证手机号，每天20条。本参数需要输入列表，默认不输入的情况下只对房间消息做出反应，单个类型也需要是列表
async def today_history(Message):  # 请保证同一个插件内不要有两个相同的指令函数名进行注册，否则只会保留最后一个注册的
    response = requests.get(historyapi).json()
    textlist = []
    for i in response["data"]["data"]:
        textlist.append(f'时间：{i["year"]}年{response["data"]["month"]}月{response["data"]["day"]}日\n'
                    f'大事件：[{i["title"]}]({i["link"]})\n')
    await API.send_msg(Message, r"\\\*"
                       '\n## 历史上的今天\n'
                       f'{newline.join(textlist)}')