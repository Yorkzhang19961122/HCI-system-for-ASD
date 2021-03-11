import asyncio

from mini.apis import errors
from mini.apis.base_api import MiniApiResultType
from mini.dns.dns_browser import WiFiDevice
from test_connect import test_connect, shutdown, test_start_run_program
from test_connect import test_get_device_by_name

from test_action import *
from test_sound import *
from test_expression import *

async def main():
    device: WiFiDevice = await test_get_device_by_name()
    if device:
        await test_connect(device)
        await test_start_run_program()

        await asyncio.sleep(5)

        ###########happy#############
        #悟空打招呼
        await test_play_tts()
        #爱心expression
        await test_play_expression()
        #我给你表演下功夫吧
        await test_play_tts1()
        #dance_002功夫
        await test_control_behavior()

        #########surprise##########
        await test_play_tts2()
        #action金鸡独立
        await test_play_action()

        await asyncio.sleep(3)
        ########sad################
        await test_play_tts3()

        await asyncio.sleep(5)
        #########action_recognition#####
        ###stand
        await test_play_tts4()
        ###挥手
        await test_play_action1()


        await test_play_tts5()
        ###深蹲
        await test_play_action2()
        await test_play_tts6()




        #await test_play_online_audio()
        #await test_play_action()
        #await asyncio.sleep(5)
        #await test_control_behavior1()

        await shutdown()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())