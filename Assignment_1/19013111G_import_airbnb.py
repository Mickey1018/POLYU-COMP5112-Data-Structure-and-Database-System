import json
import sqlite3


def start():
    """
    # import JSON into DB, airbnb.json
    # create the tables, import the data from the JSON document, store in the SQLite database
    """
    # read json file
    file = 'airbnb.json'
    with open(file, 'r', encoding="utf8") as f:
        data = f.read()

        # parse json file and convert it to python dictionary
        listing = json.loads(data)

        # create "review" table
        def import_review():

            # create connection
            conn = sqlite3.connect("airbnb.db")

            # create a cursor object
            c = conn.cursor()

            # drop existing table called "review" if any
            c.execute("DROP TABLE IF EXISTS review")

            # create a table called "review"
            c.execute('''
                CREATE TABLE review(
                id INTEGER PRIMARY KEY autoincrement, 
                rid INTEGER , 
                comment TEXT, 
                datetime TEXT, 
                accommodation_id INTEGER,
                CONSTRAINT FK_review
                FOREIGN KEY (rid) REFERENCES reviewer (rid),
                FOREIGN KEY (accommodation_id) REFERENCES accommodation (id)
                )
                ''')

            for i in listing:
                accommodation_id = i["_id"]
                reviews = i["reviews"]
                for r in reviews:
                    rid = r["reviewer_id"]
                    comment = r["comments"]
                    datetime = r["date"]["$date"]

                    # insert data into table "review"
                    c.execute("INSERT INTO review (rid, comment, datetime, accommodation_id) VALUES (?,?,?,?)",
                              (rid, comment, datetime, accommodation_id))

            # commit the action
            conn.commit()

            # close connection
            conn.close()

        # create "accommodation" table
        def import_accommodation():

            # create connection
            conn = sqlite3.connect("airbnb.db")

            # create a cursor object
            c = conn.cursor()

            # drop existing table called "accommodation" if any
            c.execute("DROP TABLE IF EXISTS accommodation")

            # create a table called "accommodation"
            c.execute('''
                        CREATE TABLE accommodation(
                        id INTEGER PRIMARY KEY, 
                        name TEXT , 
                        summary TEXT, 
                        url TEXT, 
                        review_score_value INTEGER
                        )
                        ''')

            for i in listing:
                id = i["_id"]
                name = i["name"]
                summary = i["summary"]
                url = i["listing_url"]

                # if review_scores is empty dictionary, return null
                if i["review_scores"]:
                    review_score_value = i["review_scores"]["review_scores_value"]
                else:
                    review_score_value = "NULL"

                # insert data into table "accommodation"
                c.execute("INSERT INTO accommodation (id, name, summary, url, review_score_value)\
                          VALUES (?,?,?,?,?)", (id, name, summary, url, review_score_value))

            # commit the action
            conn.commit()

            # close connection
            conn.close()

        # create "amenities" table
        def import_amenities():

            # create connection
            conn = sqlite3.connect("airbnb.db")

            # create a cursor object
            c = conn.cursor()

            # drop existing table called "amenities" if any
            c.execute("DROP TABLE IF EXISTS amenities")

            # create a table called "amenities"
            c.execute('''
                        CREATE TABLE amenities(
                        accommodation_id INTEGER, 
                        type TEXT,
                        CONSTRAINT PK_amenities
                        PRIMARY KEY(accommodation_id, type)
                        CONSTRAINT FK_amenities
                        FOREIGN KEY (accommodation_id) REFERENCES accommodation (id)
                        )
                        ''')

            for i in listing:
                accommodation_id = i["_id"]
                amenities = i["amenities"]

                # to remove the repeated amenities, update the "amenities" list
                for amenity in amenities:
                    while amenities.count(amenity) > 1:
                        amenities.remove(amenity)

                for amenity in amenities:
                    # insert data into table "amenities"
                    c.execute("INSERT INTO amenities (accommodation_id, type) VALUES (?,?)",
                              (accommodation_id, amenity))

            # commit the action
            conn.commit()

            # close connection
            conn.close()

        # create "host" table
        def import_host():

            # create connection
            conn = sqlite3.connect("airbnb.db")

            # create a cursor object
            c = conn.cursor()

            # drop existing table called "host" if any
            c.execute("DROP TABLE IF EXISTS host")

            # create a table called "host"
            c.execute('''
                        CREATE TABLE host(
                        host_id INTEGER, 
                        host_url TEXT,
                        host_name TEXT,
                        host_about TEXT,
                        host_location TEXT,
                        CONSTRAINT PK_host PRIMARY KEY (host_id)
                        )
                        ''')

            # to keep track of host_id
            visited_host_id = []

            for i in listing:
                host_id = i["host"]["host_id"]

                # only update the first occurrence of the host data
                # update visited_host_id
                if host_id not in visited_host_id:
                    visited_host_id.append(host_id)

                    host_url = i["host"]["host_url"]
                    host_name = i["host"]["host_name"]
                    host_about = i["host"]["host_about"]
                    host_location = i["host"]["host_location"]

                    # insert data into table "host"
                    c.execute("INSERT INTO host (host_id, host_url, host_name, host_about, host_location)\
                               VALUES (?,?,?,?,?)",
                              (host_id, host_url, host_name, host_about, host_location))
                else:
                    continue

            # commit the action
            conn.commit()

            # close connection
            conn.close()

        # create "host_accommodation" table
        def import_host_accommodation():

            # create connection
            conn = sqlite3.connect("airbnb.db")

            # create a cursor object
            c = conn.cursor()

            # drop existing table called "host_accommodation" if any
            c.execute("DROP TABLE IF EXISTS host_accommodation")

            # create a table called "host_accommodation"
            c.execute('''
                        CREATE TABLE host_accommodation(
                        host_id INTEGER, 
                        accommodation_id INTEGER,
                        CONSTRAINT PK_host_accommodation PRIMARY KEY (host_id, accommodation_id),
                        CONSTRAINT FK_host_accommodation
                        FOREIGN KEY (host_id) REFERENCES host (host_id)
                        FOREIGN KEY (accommodation_id) REFERENCES accommodation (id)
                        )
                        ''')

            for i in listing:
                host_id = i["host"]["host_id"]
                accommodation_id = i["_id"]

                # insert data into table "host_accommodation"
                c.execute("INSERT INTO host_accommodation (host_id, accommodation_id) VALUES (?,?)",
                          (host_id, accommodation_id))

            # commit the action
            conn.commit()

            # close connection
            conn.close()

        # create "reviewer" table
        def import_reviewer():

            # create connection
            conn = sqlite3.connect("airbnb.db")

            # create a cursor object
            c = conn.cursor()

            # drop existing table called "reviewer" if any
            c.execute("DROP TABLE IF EXISTS reviewer")

            # create a table called "reviewer"
            c.execute('''
                        CREATE TABLE reviewer(
                        rid INTEGER, 
                        rname TEXT
                        )
                        ''')

            # keep track of reviewer
            visited_rid = []

            for i in listing:
                reviews = i["reviews"]

                # loop for each review
                for review in reviews:
                    rid = review["reviewer_id"]

                    # only update the first occurrence of the reviewer data
                    # update the "visited_rid" list
                    if rid not in visited_rid:
                        visited_rid.append(rid)
                        rname = review["reviewer_name"]

                        # insert data into table "reviewer"
                        c.execute("INSERT INTO reviewer (rid, rname) VALUES (?,?)",
                                  (rid, rname))

                    else:
                        continue

            # commit the action
            conn.commit()

            # close connection
            conn.close()

        import_review()
        import_accommodation()
        import_amenities()
        import_host()
        import_host_accommodation()
        import_reviewer()


if __name__ == '__main__':
    start()