import datetime
import time
import sqlite3

def adapt_datetime(ts):
    return time.mktime(ts.timetuple())

def create_tables(file):
    
    sqlite3.register_adapter(datetime.datetime, adapt_datetime)
    conn = sqlite3.connect(file, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)

    cursor = conn.cursor()

    cursor.execute("""CREATE table user ( user_id integer primary key,
                                        username varchar unique not null,
                                        password varchar not null,
                                        salt varchar not null )""")

    cursor.execute("""CREATE table project ( project_id integer primary key,
                                            reddit_config blob,
                                            twitter_config blob,
                                            insta_config blob,
                                            user_id integer not null,
                                            foreign key(user_id) references user(user_id) )""")

    cursor.execute("""CREATE table post ( post_id string,
                                        date_uploaded_tw timestamp,
                                        date_uploaded_insta timestamp,
                                        project_id integer not null,
                                        closed boolean default false,
                                        foreign key(project_id) references project(project_id) )""")

    cursor.execute("""CREATE table twitter_followed ( user_id integer not null,
                                                    date_follow timestamp,
                                                    date_unfollow timestamp,
                                                    project_id integer not null,
                                                    foreign key(project_id) references project(project_id) )""")

    cursor.execute("""CREATE table insta_followed ( user_id integer not null,
                                                    date_follow timestamp,
                                                    date_unfollow timestamp,
                                                    project_id integer not null,
                                                    foreign key(project_id) references project(project_id) )""")

    conn.commit()
    conn.close()