def heroku_db_url(db_url):
    if db_url.startswith("mysql://"):
        db_url = "mysql+pymysql://" + db_url[len("mysql://"):]
        if db_url.endswith("?reconnect=true"):
            db_url = db_url[:-len("?reconnect=true")]
    return db_url
