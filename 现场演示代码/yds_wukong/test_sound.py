import asyncio

from mini.apis import errors
from mini.apis.api_sound import ChangeRobotVolume, ChangeRobotVolumeResponse
from mini.apis.api_sound import FetchAudioList, GetAudioListResponse, AudioSearchType
from mini.apis.api_sound import PlayAudio, PlayAudioResponse, AudioStorageType
from mini.apis.api_sound import PlayOnlineMusic, MusicResponse
from mini.apis.api_sound import PlayTTS, ControlTTSResponse, TTSControlType
from mini.apis.api_sound import StopAllAudio, StopAudioResponse
from mini.apis.base_api import MiniApiResultType
from mini.dns.dns_browser import WiFiDevice
from test_connect import test_connect, shutdown
from test_connect import test_get_device_by_name, test_start_run_program

# 测试text合成声音
async def test_play_tts():
    """测试播放tts

    使机器人开始播放一段tts，内容为"你好， 我是悟空， 啦啦啦"，并等待结果

    control_type可选TTSControlType.START/TTSControlType.STOP

    #ControlTTSResponse.isSuccess : 是否成功

    #ControlTTSResponse.resultCode : 返回码

    """
    # is_serial:串行执行
    # text:要合成的文本
    # control_type: TTSControlType.START: 播放tts; TTSControlType.STOP: 停止tts
    block: PlayTTS = PlayTTS(text="你好，我们是你的新朋友，你可以叫我悟空,这是我的朋友Tony", control_type=TTSControlType.START)

    block1: PlayTTS = PlayTTS(text="你可以试着对我们做个表情或动作", control_type=TTSControlType.START)
    # 返回元组, response是个ControlTTSResponse
    (resultType, response) = await block.execute()
    await asyncio.sleep(3)
    (resultType, response) = await block1.execute()
    #await asyncio.sleep(2)

    print(f'test_play_tts result: {response}')
    # PlayTTS block的response包含resultCode和isSuccess
    # 如果resultCode !=0 可以通过errors.get_speech_error_str(response.resultCode)) 查询错误描述信息
    print('resultCode = {0}, error = {1}'.format(response.resultCode, errors.get_speech_error_str(response.resultCode)))

    assert resultType == MiniApiResultType.Success, 'test_play_tts timetout'
    assert response is not None and isinstance(response, ControlTTSResponse), 'test_play_tts result unavailable'
    assert response.isSuccess, 'test_play_tts failed'

# 测试text合成声音
async def test_play_tts0():
    """测试播放tts

    使机器人开始播放一段tts，内容为"你好， 我是悟空， 啦啦啦"，并等待结果

    control_type可选TTSControlType.START/TTSControlType.STOP

    #ControlTTSResponse.isSuccess : 是否成功

    #ControlTTSResponse.resultCode : 返回码

    """
    # is_serial:串行执行
    # text:要合成的文本
    # control_type: TTSControlType.START: 播放tts; TTSControlType.STOP: 停止tts
    #block: PlayTTS = PlayTTS(text="你好，我是你的新朋友，你可以叫我悟空", control_type=TTSControlType.START)
    #block1: PlayTTS = PlayTTS(text="你可以试着对我做个表情或动作", control_type=TTSControlType.START)
    block2: PlayTTS = PlayTTS(text="你看起来好开心啊", control_type=TTSControlType.START)
    # 返回元组, response是个ControlTTSResponse
    #(resultType, response) = await block.execute()
    #await asyncio.sleep(2)
    #(resultType, response) = await block1.execute()
    #await asyncio.sleep(2)
    (resultType, response) = await block2.execute()

    print(f'test_play_tts result: {response}')
    # PlayTTS block的response包含resultCode和isSuccess
    # 如果resultCode !=0 可以通过errors.get_speech_error_str(response.resultCode)) 查询错误描述信息
    print('resultCode = {0}, error = {1}'.format(response.resultCode, errors.get_speech_error_str(response.resultCode)))

    assert resultType == MiniApiResultType.Success, 'test_play_tts timetout'
    assert response is not None and isinstance(response, ControlTTSResponse), 'test_play_tts result unavailable'
    assert response.isSuccess, 'test_play_tts failed'


async def test_play_tts1():

    # control_type: TTSControlType.START: 播放tts; TTSControlType.STOP: 停止tts
    block: PlayTTS = PlayTTS(text="我们给你表演下舞蹈吧", control_type=TTSControlType.START)
    # 返回元组, response是个ControlTTSResponse
    (resultType, response) = await block.execute()
    print(f'test_play_tts result: {response}')
    # PlayTTS block的response包含resultCode和isSuccess
    # 如果resultCode !=0 可以通过errors.get_speech_error_str(response.resultCode)) 查询错误描述信息
    print('resultCode = {0}, error = {1}'.format(response.resultCode, errors.get_speech_error_str(response.resultCode)))

    assert resultType == MiniApiResultType.Success, 'test_play_tts timetout'
    assert response is not None and isinstance(response, ControlTTSResponse), 'test_play_tts result unavailable'
    assert response.isSuccess, 'test_play_tts failed'

async def test_play_tts2():

    # control_type: TTSControlType.START: 播放tts; TTSControlType.STOP: 停止tts
    #block2: PlayTTS = PlayTTS(text="惊讶惊讶惊讶", control_type=TTSControlType.START)
    block: PlayTTS = PlayTTS(text="你怎么这么惊讶", control_type=TTSControlType.START)
    block1: PlayTTS = PlayTTS(text="我们不仅仅会这个呢，看我们金鸡独立", control_type=TTSControlType.START)
    # 返回元组, response是个ControlTTSResponse
    #(resultType, response) = await block2.execute()
    (resultType, response) = await block.execute()
    (resultType, response) = await block1.execute()

    print(f'test_play_tts result: {response}')
    # PlayTTS block的response包含resultCode和isSuccess
    # 如果resultCode !=0 可以通过errors.get_speech_error_str(response.resultCode)) 查询错误描述信息
    print('resultCode = {0}, error = {1}'.format(response.resultCode, errors.get_speech_error_str(response.resultCode)))

    assert resultType == MiniApiResultType.Success, 'test_play_tts timetout'
    assert response is not None and isinstance(response, ControlTTSResponse), 'test_play_tts result unavailable'
    assert response.isSuccess, 'test_play_tts failed'

async def test_play_tts3():

    # control_type: TTSControlType.START: 播放tts; TTSControlType.STOP: 停止tts
    #block3: PlayTTS = PlayTTS(text="伤心伤心伤心伤心伤心伤心", control_type=TTSControlType.START)
    block: PlayTTS = PlayTTS(text="别伤心啦，我给你讲个笑话吧", control_type=TTSControlType.START)
    block1: PlayTTS = PlayTTS(text="妈妈，老鼠跳进咱家那奶桶里了！哎呀！你把它捉出来了吗？没有，但我把咱的猫放进去了", control_type=TTSControlType.START)
    block2: PlayTTS = PlayTTS(text="怎么样，心情好点了吗", control_type=TTSControlType.START)
    # 返回元组, response是个ControlTTSResponse
    #(resultType, response) = await block3.execute()
    (resultType, response) = await block.execute()
    (resultType, response) = await block1.execute()
    await asyncio.sleep(8)
    (resultType, response) = await block2.execute()
    print(f'test_play_tts result: {response}')
    # PlayTTS block的response包含resultCode和isSuccess
    # 如果resultCode !=0 可以通过errors.get_speech_error_str(response.resultCode)) 查询错误描述信息
    print('resultCode = {0}, error = {1}'.format(response.resultCode, errors.get_speech_error_str(response.resultCode)))

    assert resultType == MiniApiResultType.Success, 'test_play_tts timetout'
    assert response is not None and isinstance(response, ControlTTSResponse), 'test_play_tts result unavailable'
    assert response.isSuccess, 'test_play_tts failed'

async def test_play_tts4():

    # control_type: TTSControlType.START: 播放tts; TTSControlType.STOP: 停止tts
    #block2: PlayTTS = PlayTTS(text="请站起来站起来吧请站起来站起来吧请站起来站起来吧", control_type=TTSControlType.START)
    block: PlayTTS = PlayTTS(text="站起来", control_type=TTSControlType.START)
    # 返回元组, response是个ControlTTSResponse
    #(resultType, response) = await block2.execute()
    (resultType, response) = await block.execute()


    print(f'test_play_tts result: {response}')
    # PlayTTS block的response包含resultCode和isSuccess
    # 如果resultCode !=0 可以通过errors.get_speech_error_str(response.resultCode)) 查询错误描述信息
    print('resultCode = {0}, error = {1}'.format(response.resultCode, errors.get_speech_error_str(response.resultCode)))

    assert resultType == MiniApiResultType.Success, 'test_play_tts timetout'
    assert response is not None and isinstance(response, ControlTTSResponse), 'test_play_tts result unavailable'
    assert response.isSuccess, 'test_play_tts failed'

async def test_play_tts5():
    # control_type: TTSControlType.START: 播放tts; TTSControlType.STOP: 停止tts
    block: PlayTTS = PlayTTS(text="向前走", control_type=TTSControlType.START)
    await asyncio.sleep(3)
    # 返回元组, response是个ControlTTSResponse
    (resultType, response) = await block.execute()

    print(f'test_play_tts result: {response}')
    # PlayTTS block的response包含resultCode和isSuccess
    # 如果resultCode !=0 可以通过errors.get_speech_error_str(response.resultCode)) 查询错误描述信息
    print('resultCode = {0}, error = {1}'.format(response.resultCode, errors.get_speech_error_str(response.resultCode)))

    assert resultType == MiniApiResultType.Success, 'test_play_tts timetout'
    assert response is not None and isinstance(response, ControlTTSResponse), 'test_play_tts result unavailable'
    assert response.isSuccess, 'test_play_tts failed'

async def test_play_tts5_1():
    # control_type: TTSControlType.START: 播放tts; TTSControlType.STOP: 停止tts
    block: PlayTTS = PlayTTS(text="换个别的动作试一下吧", control_type=TTSControlType.START)
    # 返回元组, response是个ControlTTSResponse
    (resultType, response) = await block.execute()

    print(f'test_play_tts result: {response}')
    # PlayTTS block的response包含resultCode和isSuccess
    # 如果resultCode !=0 可以通过errors.get_speech_error_str(response.resultCode)) 查询错误描述信息
    print('resultCode = {0}, error = {1}'.format(response.resultCode, errors.get_speech_error_str(response.resultCode)))

    assert resultType == MiniApiResultType.Success, 'test_play_tts timetout'
    assert response is not None and isinstance(response, ControlTTSResponse), 'test_play_tts result unavailable'
    assert response.isSuccess, 'test_play_tts failed'

async def test_play_tts6():
    # control_type: TTSControlType.START: 播放tts; TTSControlType.STOP: 停止tts
    block: PlayTTS = PlayTTS(text="请挥手", control_type=TTSControlType.START)
    # 返回元组, response是个ControlTTSResponse
    (resultType, response) = await block.execute()

    print(f'test_play_tts result: {response}')
    # PlayTTS block的response包含resultCode和isSuccess
    # 如果resultCode !=0 可以通过errors.get_speech_error_str(response.resultCode)) 查询错误描述信息
    print('resultCode = {0}, error = {1}'.format(response.resultCode, errors.get_speech_error_str(response.resultCode)))

    assert resultType == MiniApiResultType.Success, 'test_play_tts timetout'
    assert response is not None and isinstance(response, ControlTTSResponse), 'test_play_tts result unavailable'
    assert response.isSuccess, 'test_play_tts failed'

async def test_play_tts7():
    # control_type: TTSControlType.START: 播放tts; TTSControlType.STOP: 停止tts
    block: PlayTTS = PlayTTS(text="你又笑了，看来我的笑话起作用了", control_type=TTSControlType.START)
    # 返回元组, response是个ControlTTSResponse
    (resultType, response) = await block.execute()

    print(f'test_play_tts result: {response}')
    # PlayTTS block的response包含resultCode和isSuccess
    # 如果resultCode !=0 可以通过errors.get_speech_error_str(response.resultCode)) 查询错误描述信息
    print('resultCode = {0}, error = {1}'.format(response.resultCode, errors.get_speech_error_str(response.resultCode)))

    assert resultType == MiniApiResultType.Success, 'test_play_tts timetout'
    assert response is not None and isinstance(response, ControlTTSResponse), 'test_play_tts result unavailable'
    assert response.isSuccess, 'test_play_tts failed'

async def test_play_tts8():
    # control_type: TTSControlType.START: 播放tts; TTSControlType.STOP: 停止tts
    block: PlayTTS = PlayTTS(text="这个动作不太好哦", control_type=TTSControlType.START)
    # 返回元组, response是个ControlTTSResponse
    (resultType, response) = await block.execute()

    print(f'test_play_tts result: {response}')
    # PlayTTS block的response包含resultCode和isSuccess
    # 如果resultCode !=0 可以通过errors.get_speech_error_str(response.resultCode)) 查询错误描述信息
    print('resultCode = {0}, error = {1}'.format(response.resultCode,
                                                 errors.get_speech_error_str(response.resultCode)))

    assert resultType == MiniApiResultType.Success, 'test_play_tts timetout'
    assert response is not None and isinstance(response, ControlTTSResponse), 'test_play_tts result unavailable'
    assert response.isSuccess, 'test_play_tts failed'

async def test_play_tts9():
    # control_type: TTSControlType.START: 播放tts; TTSControlType.STOP: 停止tts
    block: PlayTTS = PlayTTS(text="请蹲下", control_type=TTSControlType.START)
    # 返回元组, response是个ControlTTSResponse
    (resultType, response) = await block.execute()

    print(f'test_play_tts result: {response}')
    # PlayTTS block的response包含resultCode和isSuccess
    # 如果resultCode !=0 可以通过errors.get_speech_error_str(response.resultCode)) 查询错误描述信息
    print('resultCode = {0}, error = {1}'.format(response.resultCode,
                                                 errors.get_speech_error_str(response.resultCode)))

    assert resultType == MiniApiResultType.Success, 'test_play_tts timetout'
    assert response is not None and isinstance(response, ControlTTSResponse), 'test_play_tts result unavailable'
    assert response.isSuccess, 'test_play_tts failed'

async def test_play_tts10():
    # control_type: TTSControlType.START: 播放tts; TTSControlType.STOP: 停止tts
    block: PlayTTS = PlayTTS(text="请踢腿", control_type=TTSControlType.START)
    # 返回元组, response是个ControlTTSResponse
    (resultType, response) = await block.execute()

    print(f'test_play_tts result: {response}')
    # PlayTTS block的response包含resultCode和isSuccess
    # 如果resultCode !=0 可以通过errors.get_speech_error_str(response.resultCode)) 查询错误描述信息
    print('resultCode = {0}, error = {1}'.format(response.resultCode,
                                                 errors.get_speech_error_str(response.resultCode)))

    assert resultType == MiniApiResultType.Success, 'test_play_tts timetout'
    assert response is not None and isinstance(response, ControlTTSResponse), 'test_play_tts result unavailable'
    assert response.isSuccess, 'test_play_tts failed'

# 测试播放音效(在线)
async def test_play_online_audio():
    """测试播放在线音效

    使机器人播放一段在线音效，地址为"http://yun.lnpan.com/music/download/ring/000/075/5653bae83917a892589b372782175dd8.amr"

    并等待结果

    #PlayAudioResponse.isSuccess : 是否成功

    #PlayAudioResponse.resultCode : 返回码

    """
    # 播放音效, url表示要播放的音效列表
    block: PlayAudio = PlayAudio(
        url="http://m701.music.126.net/20200716202257/96afe9e97970c4ff21049189c2611010/jdymusic/obj/w5zDlMODwrDDiGjCn8Ky/1497471810/ae4f/3676/98a8/c98c5b9f5350b8dcb34dfb81f94e73ec.mp3",
        storage_type=AudioStorageType.NET_PUBLIC)
    # response是个PlayAudioResponse
    (resultType, response) = await block.execute()

    # await asyncio.sleep(3)
    #
    # # 停止所有声音
    # block: StopAllAudio = StopAllAudio()
    # (resultType, response) = await block.execute()

    print(f'test_play_online_audio result: {response}')
    print('resultCode = {0}, error = {1}'.format(response.resultCode, errors.get_speech_error_str(response.resultCode)))

    assert resultType == MiniApiResultType.Success, 'test_play_online_audio timetout'
    assert response is not None and isinstance(response, PlayAudioResponse), 'test_play_online_audio result unavailable'
    assert response.isSuccess, 'test_play_online_audio failed'


async def test_play_local_audio():
    """测试播放本地音效

    使机器人播放一段本地内置音效，音效名称为"read_016"，并等待结果

    #PlayAudioResponse.isSuccess : 是否成功

    #PlayAudioResponse.resultCode : 返回码

    """

    block: PlayAudio = PlayAudio(
        url="read_016",
        storage_type=AudioStorageType.PRESET_LOCAL)
    # response是个PlayAudioResponse
    (resultType, response) = await block.execute()

    print(f'test_play_local_audio result: {response}')
    print('resultCode = {0}, error = {1}'.format(response.resultCode, errors.get_speech_error_str(response.resultCode)))

    assert resultType == MiniApiResultType.Success, 'test_play_local_audio timetout'
    assert response is not None and isinstance(response, PlayAudioResponse), 'test_play_local_audio result unavailable'
    assert response.isSuccess, 'test_play_local_audio failed'


# 测试获取机器人的音效资源
async def test_get_audio_list():
    """测试获取音效列表

    获取机器人内置的音效列表，并等待结果

    #GetAudioListResponse.audio ([Audio]) : 音效列表
    #Audio.name : 音效名
    #Audio.suffix : 音效后缀

    #GetAudioListResponse.isSuccess : 是否成功

    #GetAudioListResponse.resultCode : 返回码

    """
    # search_type: AudioSearchType.INNER 是指机器人内置的不可修改的音效, AudioSearchType.CUSTOM 是放置在sdcard/customize/music目录下可别开发者修改的音效
    block: FetchAudioList = FetchAudioList(search_type=AudioSearchType.INNER)
    # response是个GetAudioListResponse
    (resultType, response) = await block.execute()

    print(f'test_get_audio_list result: {response}')

    assert resultType == MiniApiResultType.Success, 'test_get_audio_list timetout'
    assert response is not None and isinstance(response, GetAudioListResponse), 'test_play_audio result unavailable'
    assert response.isSuccess, 'test_get_audio_list failed'


# 测试停止正在播放的tts
async def test_stop_audio_tts():
    """测试停止所有正在播放的音频

    先播放一段tts，3s后，停止所有所有音效，并等待结果

    #StopAudioResponse.isSuccess : 是否成功　

    #StopAudioResponse.resultCode : 返回码

    """
    # 设置is_serial=False, 表示只需将指令发送给机器人,await不需要等机器人执行完结果再返回
    block: PlayTTS = PlayTTS(is_serial=False, text="你让我说，让我说，不要打断我，你让我说，让我说，不要打断我")
    response = await block.execute()
    print(f'test_stop_audio.play_tts: {response}')
    await asyncio.sleep(3)

    # 停止所有声音
    block: StopAllAudio = StopAllAudio()
    (resultType, response) = await block.execute()

    print(f'test_stop_audio:{response}')

    assert resultType == MiniApiResultType.Success, 'test_stop_audio timetout'
    assert response is not None and isinstance(response, StopAudioResponse), 'test_stop_audio result unavailable'
    assert response.isSuccess, 'test_stop_audio failed'


# 测试停止正在播放的onlineMusic
async def test_stop_audio_online_music():
    """测试停止所有正在播放的音频

    先播放在线音乐，10s后，停止所有所有音效，并等待结果

    #StopAudioResponse.isSuccess : 是否成功　

    #StopAudioResponse.resultCode : 返回码

    """
    # 设置is_serial=False, 表示只需将指令发送给机器人,await不需要等机器人执行完结果再返回
    # block: PlayOnlineMusic = PlayOnlineMusic(is_serial=False, name='我的世界')
    # response = await block.execute()
    # print(f'test_stop_audio.play_online_music: {response}')


    await asyncio.sleep(10)

    # 停止所有声音
    block: StopAllAudio = StopAllAudio()
    (resultType, response) = await block.execute()

    print(f'test_stop_audio:{response}')

    assert resultType == MiniApiResultType.Success, 'test_stop_audio timetout'
    assert response is not None and isinstance(response, StopAudioResponse), 'test_stop_audio result unavailable'
    assert response.isSuccess, 'test_stop_audio failed'


# 测试播放一首音乐
async def test_play_online_music():
    """测试播放在线歌曲

    使机器人播放在线歌曲"我的世界"，并等待结果
    播放qq音乐, 需要在手机端授权

    #MusicResponse.isSuccess : 是否成功

    #MusicResponse.resultCode : 返回码

    """
    # 播放qq音乐, 需要在手机端授权
    block: PlayOnlineMusic = PlayOnlineMusic(name='入海')
    (resultType, response) = await block.execute()

    print(f'test_play_online_music result: {response}')

    assert resultType == MiniApiResultType.Success, 'test_play_online_music timetout'
    assert response is not None and isinstance(response, MusicResponse), 'test_play_online_music result unavailable'
    assert response.isSuccess, 'test_play_online_music failed'

# 测试, 改变机器人的音量
async def test_change_robot_volume():
    """调整机器人音量demo

    设置机器人音量为0.5，等待回复结果

    #ChangeRobotVolumeResponse.isSuccess : 是否成功

    #ChangeRobotVolumeResponse.resultCode : 返回码

    """
    # volume: 0~1.0
    block: ChangeRobotVolume = ChangeRobotVolume(volume=0.5)
    # response:ChangeRobotVolumeResponse
    (resultType, response) = await block.execute()

    print(f'test_change_robot_volume result:{response}')

    assert resultType == MiniApiResultType.Success, 'test_change_robot_volume timetout'
    assert response is not None and isinstance(response,
                                               ChangeRobotVolumeResponse), 'test_change_robot_volume result unavailable'
    assert response.isSuccess, 'get_action_list failed'


if __name__ == '__main__':
    device: WiFiDevice = asyncio.get_event_loop().run_until_complete(test_get_device_by_name())
    if device:
        asyncio.get_event_loop().run_until_complete(test_connect(device))
        asyncio.get_event_loop().run_until_complete(test_start_run_program())

        asyncio.get_event_loop().run_until_complete(test_play_tts())
        #asyncio.get_event_loop().run_until_complete(test_get_audio_list())
        #asyncio.get_event_loop().run_until_complete(test_play_local_audio())
        asyncio.get_event_loop().run_until_complete(test_play_online_audio())
        #asyncio.get_event_loop().run_until_complete(test_play_online_music())
        #asyncio.get_event_loop().run_until_complete(test_stop_audio_tts())
        #asyncio.get_event_loop().run_until_complete(test_stop_audio_online_music())
        #asyncio.get_event_loop().run_until_complete(test_change_robot_volume())
        asyncio.get_event_loop().run_until_complete(shutdown())
