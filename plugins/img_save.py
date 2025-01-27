import os
from io import BytesIO

from botpy.ext.cog_yaml import read
import requests
from sqlalchemy import Column, Integer, String, Date, create_engine, text
from sqlalchemy.orm import sessionmaker

from plugins.user_todo_list import insert

config = read(os.path.join(os.path.dirname(__file__), "../config.yaml"))


# Description: Image save plugin
class QrSj:
    __tablename__ = 'qr_sj'
    id = Column(Integer, primary_key=True)
    img_path = ""
    img_name = ""
    img_note = ""
    img_seq = 0
    url_get = ""
    url_delete = ""
    upload_by = ""
    upload_time = ""
    belong_group = ""
    is_deleted = 0
    group_id = 0

    def __repr__(self):
        return (
            "QrSj(id:{},img_path:{},img_name:{},img_note:{},img_seq:{},url_get:{},url_delete:{},upload_by:{},upload_time:{})"
            .format(self.id, self.img_path, self.img_name, self.img_note, self.img_seq, self.url_get, self.url_delete,
                    self.upload_by, self.upload_time))

    def imgUpload(self, file_data):
        headers = {'Authorization': config['picturesToken']}
        img_stream = BytesIO(file_data)
        img_stream.name = self.img_name
        files = {'smfile': img_stream}
        url = 'https://sm.ms/api/v2/upload'
        res = requests.post(url, files=files, headers=headers).json()
        if res.get('code') != 'success':
            print("[Error] Upload image failed.")
            return res.get('code')
        data = res.get('data')
        self.url_get = data.get('url')
        self.url_delete = data.get('delete')
        print("[Info] File image URL is: " + self.url_get)
        return "True"


class SqliteSqlalchemy(object):
    def __init__(self):
        # 创建Sqlite连接引擎
        # self.engine = create_engine('sqlite:///../database/chat_bot.db', echo=True)
        self.engine = create_engine('sqlite:///./database/chat_bot.db', echo=True)
        # 创建Sqlite的session连接对象
        self.session = sessionmaker(bind=self.engine)()


insertSjImage = text(
    "insert into qr_sj ( img_name, img_note,  url_get, url_delete, upload_by, upload_time,belong_group,group_id) "
    "values ( :img_name, :img_note,  :url_get, :url_delete, :upload_by, :upload_time,:belong_group,:group_id)")
selectGroupMax = text("select max(group_id) from qr_sj where belong_group = :belong_group")


def insertSj(qr_sj):
    session = SqliteSqlalchemy().session
    maxId = session.execute(selectGroupMax, {'belong_group': qr_sj[0].belong_group}).fetchone()[0]
    if maxId is None:
        maxId = 0
    for sj in qr_sj:
        maxId += 1
        session.execute(insertSjImage,
                        {'img_path': sj.img_path, 'img_name': sj.img_name, 'img_note': sj.img_note,
                         'img_seq': sj.img_seq, 'url_get': sj.url_get, 'url_delete': sj.url_delete,
                         'upload_by': sj.upload_by, 'upload_time': sj.upload_time,
                         'belong_group': sj.belong_group, 'group_id': maxId})

        session.commit()
        session.close()
        return


def changeNote(id, belong_group, new_note):
    session = SqliteSqlalchemy().session
    session.execute(text("update qr_sj set img_note = :new_note where group_id = :id and belong_group = :belong_group"),
                    {'new_note': new_note, 'id': id, 'belong_group': belong_group})
    session.commit()
    session.close()
    return True


if __name__ == '__main__':
    sj = QrSj()
    sj.img_path = 'test'
    sj.img_name = 'test'
    sj.img_note = 'test'
    sj.img_seq = 1
    sj.upload_by = 'test'
    sj.upload_time = '2021-01-01'
    sj.belong_group = 'test'
    sj.url_get = 'test'
    sj.url_delete = 'test'
    insertSj(sj)
