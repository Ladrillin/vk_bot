import sqlite3
import time

conn = sqlite3.connect('vk_db_for_reminder.db')
c = conn.cursor()

def update(row, variable):
    cmd = "UPDATE Reminder SET %s = %d" % (row, variable)
    c.execute(cmd)
    conn.commit()

def select_one():
    cmd = 'SELECT Epoch_Time FROM Reminder'
    c.execute(cmd)
    result = c.fetchone()
    print(result)

def reminder():
    for i in range(0, 2):
        if select_one() == 0:
            update('Existence', 1)
        else:
            current_epoch_time = int(time.time())
            past_epoch_time = int(select_one())
            if (current_epoch_time - past_epoch_time) > (30):
                print('Reminder')
                update('Epoch_Time', current_epoch_time)
        break