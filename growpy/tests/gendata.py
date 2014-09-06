from growpy.persistence.store import Store
from growpy.persistence.orm import Status
from calendar import monthrange
from datetime import datetime
from sqlalchemy import desc
from random import choice
store = Store()

factor = [.1, .4, .6, .10, -.4, -.10]

seed = 12 * 1024 * 1024


def fill_stat(fs):
    for y in range(2012, 2015):
        for x in range(1, 13):
            last_day = monthrange(y, x)[1] + 1
            for d in range(1, last_day):
                str_date = str(y)
                if x < 10:
                    str_date += '0' + str(x)
                else:
                    str_date += str(x)
                if d < 10:
                    str_date += '0' + str(d)
                else:
                    str_date += str(d)
                str_date += ' 00:00:00'
                date = datetime.strptime(str_date, '%Y%m%d %H:%M:%S')
                latest = store.session.query(Status).filter(Status.fs_id == fs.fs_id).\
                    order_by(desc(Status.status_date)).first()
                if fs.fs_pmount == '/':
                    if latest == None:
                        size = seed
                        add = 8 * 1024 * 1024
                    else:
                        add = (latest.status_used * choice(factor)) / last_day
                        add += latest.status_used
                        if add > latest.status_size:
                            size = round(latest.status_size * .40, 0)
                            size += latest.status_size
                        else:
                            size = latest.status_size
                elif fs.fs_pmount == '/boot':
                    size = 512 * 1024
                    add = 12 * 1024
                else:
                    size = 1024 * 1024
                    add = 1024
                try:
                    st = Status(fs.fs_id, size, add, date)
                    store.session.add(st)
                    store.session.commit()
                except Exception as e:
                    print(e)

if __name__ == '__main__':
    from datetime import datetime
    gt = datetime.now()
    for n in store.get_node_list():
        for fs in store.get_fs_list(n):
            print(n.node_name, fs.fs_pmount)
            latest = store.session.query(Status).filter(Status.fs_id == fs.fs_id).\
                order_by(desc(Status.status_date)).first()
            fill_stat(fs)
    print(datetime.now() - gt)