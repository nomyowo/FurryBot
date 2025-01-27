import os
import random
from botpy.ext.cog_yaml import read

from sqlalchemy import text

from plugins.img_save import SqliteSqlalchemy

selectCurrentGroupSj = text("select * from qr_sj where belong_group = :belong_group AND is_deleted = 0;")
selectGroupSjByNote = text(
    "select * from qr_sj where img_note like :img_note AND belong_group = :belong_group AND is_deleted = 0;")
config = read(os.path.join(os.path.dirname(__file__), "../config.yaml"))


def sjGet(belong_group):
    session = SqliteSqlalchemy().session
    sj_list = session.execute(selectCurrentGroupSj, {'belong_group': belong_group}).fetchall()
    random_sj = random.choice(sj_list)
    return random_sj


def sjGetByNote(belong_group, img_note):
    session = SqliteSqlalchemy().session
    sj_list = session.execute(selectGroupSjByNote,
                              {'belong_group': belong_group, 'img_note': '%' + img_note + '%'}).fetchall()
    if len(sj_list) == 0:
        return None
    random_sj = random.choice(sj_list)
    return random_sj


if __name__ == '__main__':
    print(sjGet('AC4A46DC4E54F980F941712A171F7857'))
