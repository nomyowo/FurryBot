# -*- coding: utf-8 -*-
import os
import socket

import botpy
import requests
import uuid
import re
from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.message import GroupMessage

from plugins import weather_api, img_upload, fortune_by_sqlite, user_todo_list, ai_chat
from openai import OpenAI

from plugins.img_save import QrSj, insertSj, changeNote
from plugins.sj_get import sjGet, sjGetByNote

config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()


class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    # 判断数据库初是否始化
    fortune_by_sqlite.database_initialized()
    # 建立ai客户端
    ai_client = OpenAI(api_key=config["api_key"], base_url="https://api.deepseek.com")

    async def on_group_at_message_create(self, message: GroupMessage):
        msg = message.content.strip()
        member_openid = message.author.member_openid
        print("[Info] bot 收到消息：" + message.content)

        if msg == f"我喜欢你":
            messageResult = await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=0,
                msg_id=message.id,
                content=f"我也喜欢你")

        elif msg.startswith("/今日运势"):
            result = fortune_by_sqlite.get_today_fortune(member_openid)
            file_url = img_upload.get_upload_history()
            # print(result)
            messageResult = await message._api.post_group_file(
                group_openid=message.group_openid,
                file_type=1,
                url=file_url
            )
            # 资源上传后，会得到Media，用于发送消息
            await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=7,
                msg_id=message.id,
                media=messageResult,
                content=f"{result}"
            )

        elif msg.startswith("/聊天"):
            messageResult = await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=0,
                msg_id=message.id,
                content=ai_chat.chatService(self.ai_client, msg.replace("/聊天", "").strip())
            )

        elif msg.startswith("/sj") or msg.startswith("/圣经"):
            msg_next = msg.replace("/sj", "").replace("/圣经", "").strip()
            author = message.author.__dict__
            # 若/圣经后未添加参数，则全局搜索
            if msg_next == "":
                random_sj = sjGet(message.group_openid)
                messageResult = await message._api.post_group_file(
                    group_openid=message.group_openid,
                    file_type=1,
                    url=random_sj.url_get
                )
                await message._api.post_group_message(
                    group_openid=message.group_openid,
                    msg_type=7,
                    msg_id=message.id,
                    media=messageResult,
                    content=f"id = {str(random_sj.group_id)}\n{'标签：#' + random_sj.img_note if random_sj.img_note != '' else '无备注'}"
                )

            # 若/圣经后添加参数，则通过标签查找圣经
            else:
                random_sj = sjGetByNote(message.group_openid, msg_next.replace("-n", "").strip())
                if (random_sj is None):
                    messageResult = await message._api.post_group_message(
                        group_openid=message.group_openid,
                        msg_type=0,
                        msg_id=message.id,
                        content="该标签没有找到圣经诶qwqqqqqq"
                    )
                else:
                    messageResult = await message._api.post_group_file(
                        group_openid=message.group_openid,
                        file_type=1,
                        url=random_sj.url_get
                    )
                    await message._api.post_group_message(
                        group_openid=message.group_openid,
                        msg_type=7,
                        msg_id=message.id,
                        media=messageResult,
                        content=f"id = {str(random_sj.group_id)}\n{'标签：#' + random_sj.img_note if random_sj.img_note != '' and random_sj.img_note is not None else '无备注'}"
                    )

        elif msg.startswith("/tj") or msg.startswith("/添加"):
            msg_next = msg.replace("/tj", "").replace("/添加", "").strip()
            if msg_next.startswith("-n"):
                params = msg_next.replace("-n", "").replace("：", ":").strip().split(":")
                id = params[0]
                note = params[1]
                if changeNote(id, message.group_openid, note):
                    messageResult = await message._api.post_group_message(
                        group_openid=message.group_openid,
                        msg_type=0,
                        msg_id=message.id,
                        content="标签变更成功"
                    )
            else:
                if len(message.attachments) == 0:
                    messageResult = await message._api.post_group_message(
                        group_openid=message.group_openid,
                        msg_type=0,
                        msg_id=message.id,
                        content="请添加图片"
                    )
                else:
                    uploadBy = message.author.member_openid
                    belongGroup = message.group_openid
                    uploadTime = message.timestamp
                    # 读取图片备注
                    imgNoteStr = msg.replace("/tj", "").replace("/添加", "").replace(" ", "").strip()
                    imgNotes = re.split(r'[,;，；]', imgNoteStr)
                    print(imgNotes)
                    # 读取message中图片url，并上传至图床
                    images = []
                    for i in range(len(message.attachments)):
                        image = QrSj()
                        image.img_name = str(uuid.uuid4())
                        image.img_note = imgNotes[i] if i < len(imgNotes) else ""
                        image.upload_by = uploadBy
                        image.belong_group = belongGroup
                        image.upload_time = uploadTime
                        # 下载图片
                        res = requests.get(message.attachments[i].url)
                        # 上传图片
                        uploadRes = image.imgUpload(res.content)
                        if uploadRes == "True":
                            # 组合图片信息
                            images.append(image)
                        else:
                            # 上传失败
                            messageResult = await message._api.post_group_message(
                                group_openid=message.group_openid,
                                msg_type=0,
                                msg_id=message.id,
                                content=uploadRes
                            )
                            return None
                    print(images)
                    insertSj(images)
                    messageResult = await message._api.post_group_message(
                        group_openid=message.group_openid,
                        msg_type=0,
                        msg_id=message.id,
                        content="圣经添加成功"
                    )


        elif msg.startswith("/test"):
            messageResult = await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=0,
                msg_id=message.id,
                content=f"\nBoost & Magnum, ready fight!!!")

        elif msg.startswith("/天气"):
            city_name = msg.replace("/天气", "").strip()
            result = weather_api.format_weather(city_name)
            messageResult = await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=0,
                msg_id=message.id,
                content=f"{result}")

        elif msg.startswith("/查询"):
            file_url = img_upload.upload('../examples/imgs/img_test.jpg')  # 此处填写你要上传图片的地址
            # file_url = f"https://s21.ax1x.com/2024/12/08/pA7DmAP.jpg"  # 这里需要填写上传的资源Url

            messageResult = await message._api.post_group_file(
                group_openid=message.group_openid,
                file_type=1,  # 文件类型要对应上，具体支持的类型见方法说明
                url=file_url  # 文件Url
            )

            # 资源上传后，会得到Media，用于发送消息
            await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=7,  # 7表示富媒体类型
                msg_id=message.id,
                media=messageResult
            )
            img_upload.delete_img()  # 从图床中删除图片，防止重复上传

        elif msg.startswith("/help"):
            content = "\n" + '\n\n\'/今日运势\' 的用法：\n  @机器人后输入 /今日运势\n示例：@FurryBot /今日运势\n'\
                '\n\n\'/圣经\' 的用法：\n  @机器人后输入 /圣经 即可返回一条圣经\n  也可输入 -n 标签 根据标签查找圣经\n示例：@FurryBot /圣经 或 @FurryBot /圣经 小狗\n'\
                '\n\n\'/添加\' 的用法：\n  选择一张或多张照片，@机器人后输入 /添加 或 /tj 自动添加圣经\n  可以在 /添加 给图片添加标签，用逗号分隔即可\n  若需更改标签，在 /添加 后输入 -n 图片id:新标签 即可\n示例：@FurryBot /添加 小狗 或 @FurryBot -n 1：小狗\n'\
                '\n\n\'/天气\' 的用法：\n  @机器人后输入 /天气 城市，返回所需城市天气\n示例：@FurryBot /天气 北京\n'\
                '\n\n\'/聊天\' 的用法：\n  @机器人后输入 /聊天 您的问题，或直接@机器人后输入您的问题\n示例：@FurryBot /聊天 你是谁 或 @FurryBot 你是谁\n'
            messageResult = await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=0,
                msg_id=message.id,
                content=content)
        elif msg.startswith("/待办"):
            msgs = msg.replace("/待办", "").strip()
            author = message.author.__dict__

            msg_user = author['member_openid']
            print('[Info] message author is: ' + msg_user)
            if msgs.startswith("-s"):
                todo_list = user_todo_list.show(msg_user)
                if todo_list == -1:
                    content1 = '没有查询到该用户的待办呢。\n已为您创建用户。'
                else:
                    content1 = '\n待办有如下哦：\n'
                    for todo in todo_list:
                        todo = '\n' + todo + '\n'
                        content1 = content1 + todo

                messageResult = await message._api.post_group_message(
                    group_openid=message.group_openid,
                    msg_type=0,
                    msg_id=message.id,
                    content=content1)

            elif msgs.startswith("-d"):
                msg_all = msgs.replace("-d", "").strip()
                msg_num = msg_all
                flag = user_todo_list.delete(msg_user, int(msg_num))
                if flag == 1:
                    messageResult = await message._api.post_group_message(
                        group_openid=message.group_openid,
                        msg_type=0,
                        msg_id=message.id,
                        content=f"成功删除第{msg_num}条待办")
                elif flag == -2:
                    messageResult = await message._api.post_group_message(
                        group_openid=message.group_openid,
                        msg_type=0,
                        msg_id=message.id,
                        content=f"不存在这条待办哦")
                else:
                    messageResult = await message._api.post_group_message(
                        group_openid=message.group_openid,
                        msg_type=0,
                        msg_id=message.id,
                        content='没有查询到该用户的待办呢。\n已为您创建用户。')
            elif msgs.startswith("-i"):
                msg_todo = msgs.replace("-i", "").strip()
                flag = user_todo_list.insert(msg_user, msg_todo)
                if flag == 1:
                    messageResult = await message._api.post_group_message(
                        group_openid=message.group_openid,
                        msg_type=0,
                        msg_id=message.id,
                        content=f"成功添加待办，今后也要加油哦(ง •_•)ง")
                else:
                    messageResult = await message._api.post_group_message(
                        group_openid=message.group_openid,
                        msg_type=0,
                        msg_id=message.id,
                        content='没有查询到该用户的待办呢。\n已为您创建用户。')
            elif msgs.startswith("-clear"):
                flag = user_todo_list.init(msg_user)
                if flag == 1:
                    messageResult = await message._api.post_group_message(
                        group_openid=message.group_openid,
                        msg_type=0,
                        msg_id=message.id,
                        content='已为您成功清除所有待办！')
                else:
                    messageResult = await message._api.post_group_message(
                        group_openid=message.group_openid,
                        msg_type=0,
                        msg_id=message.id,
                        content='没有查询到该用户的待办呢。\n已为您创建用户。')

            else:
                content2 = '\n\n\'/待办\' 的用法：\n  \'-s\'显示您所有待办\n  \'-d 序号\' 删除第几条待办 \n  \'-i\' 添加待办\n  \'-clear\' 清除所有待办'
                messageResult = await message._api.post_group_message(
                    group_openid=message.group_openid,
                    msg_type=0,
                    msg_id=message.id,
                    content=content2)

        else:
            print("Chat")
            messageResult = await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=0,
                msg_id=message.id,
                content=ai_chat.chatService(self.ai_client, msg.strip())
            )

        _log.info(messageResult)


if __name__ == "__main__":
    # 通过预设置的类型，设置需要监听的事件通道
    # intents = botpy.Intents.none()
    # intents.public_messages=True

    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(public_messages=True)
    client = MyClient(intents=intents, is_sandbox=True)
    client.run(appid=config["appid"], secret=config["secret"])

    # print(config["help"])
