from flask import Flask, request, jsonify
import json
import sqlite3

app = Flask(__name__)
app.config['DEBUG'] = True


# (a) Show your student ID
@app.route('/mystudentID/', methods=['GET'])
def my_student_id():
    response = {"studentID": "19013111G"}
    return jsonify(response), 200, {'Content-Type': 'application/json'}


# (b) Get all reviews
@app.route('/airbnb/reviews/', methods=['GET'])
def get_reviews():

    # create connection
    conn = sqlite3.connect("airbnb.db")

    # create a cursor object
    db = conn.cursor()

    # get total review count
    query_1 = "SELECT count(id) FROM review"
    result_1 = db.execute(query_1).fetchall()

    count = []
    for row in result_1:
        count.append(row)

    # get reviews information
    query_2 = "SELECT accommodation_id, comment, datetime, review.rid, rname " \
              "FROM 'review' join 'reviewer' on review.rid = reviewer.rid " \
              "ORDER BY datetime DESC, review.rid ASC"
    result_2 = db.execute(query_2).fetchall()

    reviews = []
    for row in result_2:
        reviews.append({
            "Accommodation ID": row[0],
            "Comment": row[1],
            "DateTime": row[2],
            "Reviewer ID": row[3],
            "Reviewer Name": row[4]
        })

    # close connection
    conn.close()

    # store the results in dictionary
    results = {"Count": count[0][0], "Reviews": reviews}

    # convert to json format
    j = json.dumps(results)

    return j, 200, {'Content-Type': 'application/json'}


# (c.1) Get all reviewers
@app.route('/airbnb/reviewers/', methods=['GET'])
def get_reviewers():

    # create connection
    conn = sqlite3.connect("airbnb.db")

    # create a cursor object
    db = conn.cursor()

    # get total reviewer count
    query_1 = "SELECT count(rid) FROM reviewer"
    result_1 = db.execute(query_1).fetchall()

    count = []
    for row in result_1:
        count.append(row)

    # get reviewers information
    query_2 = """SELECT count(review.rid), review.rid, rname
                 FROM 'review' join 'reviewer' on review.rid = reviewer.rid
                 GROUP BY review.rid
                 ORDER BY review.rid ASC"""
    result_2 = db.execute(query_2).fetchall()

    reviews = []
    for row in result_2:
        reviews.append({
            "Review Count": row[0],
            "Reviewer ID": row[1],
            "Reviewer Name": row[2],
        })

    # close connection
    conn.close()

    # store the results in dictionary
    results = {"Count": count[0][0], "Reviewers": reviews}

    # convert to json format
    j = json.dumps(results)

    return j, 200, {'Content-Type': 'application/json'}


# (c.2) Getting a reviewer and his/her review
@app.route('/airbnb/reviewers/<rid>', methods=['GET'])
def get_reviewer_and_review(rid):

    # create connection
    conn = sqlite3.connect("airbnb.db")

    # create a cursor object
    db = conn.cursor()

    # get all reviewer ID
    query_1 = "SELECT rid FROM reviewer"
    result_1 = db.execute(query_1).fetchall()
    all_rid = []
    for row in result_1:
        all_rid.append(row[0])

    # get reviewer name
    query_2 = "SELECT rname FROM reviewer WHERE rid = ?"
    result_2 = db.execute(query_2, [rid]).fetchall()
    name = []
    for row in result_2:
        name.append(row)

    # get reviews
    query_3 = "SELECT accommodation_id, comment, datetime FROM 'review' where rid = ? order by datetime desc"
    result_3 = db.execute(query_3, [rid]).fetchall()
    reviews = []
    for row in result_3:
        reviews.append({
            "Accommodation ID": row[0],
            "Comment": row[1],
            "Datetime": row[2]
        })

    # close connection
    conn.close()

    if int(rid) in all_rid:

        # store the results in dictionary
        results = {"Reviewer ID": rid,
                   "Reviewer Name": name[0][0],
                   "Reviews": reviews}

        # convert to json format
        j = json.dumps(results)

        return j, 200, {'Content-Type': 'application/json'}

    else:
        return jsonify({"Reasons": [
            {'Message': 'Reviewer not found'}
        ]}), 404


# (d.1) get all hosts
@app.route('/airbnb/hosts/', methods=['GET'])
def get_hosts():

    # create connection
    conn = sqlite3.connect("airbnb.db")

    # create a cursor object
    db = conn.cursor()

    # get host count
    query_1 = "SELECT count(host_id) FROM host"
    result_1 = db.execute(query_1).fetchall()
    all_host = []
    for row in result_1:
        all_host.append(row[0])

    # get host information
    query_2 = """
    SELECT count(host_accommodation.accommodation_id), host_about, host.host_id, host_location, host_name, host_url
    FROM 'host_accommodation' 
    JOIN host ON host_accommodation.host_id = host.host_id
    group by host.host_id
    order by host.host_id
    """
    result_2 = db.execute(query_2).fetchall()
    hosts = []
    for row in result_2:
        hosts.append({
            "Accommodation Count": row[0],
            "Host About": row[1],
            "Host ID": row[2],
            "Host Location": row[3],
            "Host Name": row[4],
            "Host URL": row[5]
        })

    # close connection
    conn.close()

    # store the results in dictionary
    results = {"Count": all_host[0],
               "Hosts": hosts
               }

    # convert to json format
    j = json.dumps(results)

    return j, 200, {'Content-Type': 'application/json'}


# (d.2) get a host by ID
@app.route('/airbnb/hosts/<host_id>', methods=['GET'])
def get_host_by_id(host_id):

    # create connection
    conn = sqlite3.connect("airbnb.db")

    # create a cursor object
    db = conn.cursor()

    # get all host ID
    query_1 = "SELECT host_id FROM host"
    result_1 = db.execute(query_1).fetchall()
    all_host = []
    for row in result_1:
        all_host.append(row[0])

    # get accommodation information
    query_2 = """
    SELECT accommodation.id, name
    FROM 'accommodation' 
    join host_accommodation on accommodation.id = host_accommodation.accommodation_id
    where host_id = ?
    order by id ASC"""
    result_2 = db.execute(query_2, [host_id]).fetchall()
    accommodations = []
    for row in result_2:
        accommodations.append({
            "Accommodation ID": row[0],
            "Accommodation Name": row[1]
        })

    # get host information
    query_3 = """
    SELECT count(host.host_id), host_about, host.host_id, host_location, host_name, host_url
    FROM 'host' 
    join host_accommodation on host.host_id = host_accommodation.host_id
    where host.host_id = ?"""
    result_3 = db.execute(query_3, [host_id]).fetchall()
    host = []
    for row in result_3:
        host.append(row)

    # close connection
    conn.close()

    if int(host_id) in all_host:

        # store the results in dictionary
        results = {"Accommodation": accommodations,
                   "Accommodation Count": host[0][0],
                   "Host About": host[0][1],
                   "Host ID": host[0][2],
                   "Host Location": host[0][3],
                   "Host Name": host[0][4],
                   "Host URL": host[0][5]
                   }

        # convert to json format
        j = json.dumps(results)

        return j, 200, {'Content-Type': 'application/json'}

    else:
        return jsonify({"Reasons": [
            {'Message': 'Host not found'}
        ]}), 404


# (e.1) get all accommodation
@app.route('/airbnb/accommodations/', methods=['GET'])
def get_accommodation():

    # create connection
    conn = sqlite3.connect("airbnb.db")

    # create a cursor object
    db = conn.cursor()

    # get all accommodation information
    query_1 = """
    SELECT name, summary, url, type, host_about, host.host_id, host_location, host_name, accommodation.id, count(), review_score_value 
    FROM 'accommodation' 
    join (select accommodation_id, group_concat(type) as type
    from amenities
    group by accommodation_id) t on t.accommodation_id = accommodation.id
    join review on review.accommodation_id = accommodation.id
    join host_accommodation on host_accommodation.accommodation_id = accommodation.id
    join host on host_accommodation.host_id = host.host_id
    group by accommodation.id
    order by accommodation.id asc
    """
    result_1 = db.execute(query_1).fetchall()
    accommodations = []
    for row in result_1:
        accommodations.append({
            "Accommodation": {
                "Name": row[0],
                "Summary": row[1],
                "URL": row[2]
            },
            "Amenities": convert(row[3]),
            "Host": {
                "About": row[4],
                "ID": row[5],
                "Location": row[6],
                "Name": row[7]
            },
            "ID": row[8],
            "Review Count": row[9],
            "Review Score Value": row[10]
        })

    # get accommodation count
    query_2 = """SELECT count(id) FROM accommodation"""
    result_2 = db.execute(query_2).fetchall()
    count = []
    for row in result_2:
        count.append(row)

    # close connection
    conn.close()

    # store the results in dictionary
    results = {"Accommodations": accommodations,
               "Count": count[0][0]
               }

    # convert to json format
    j = json.dumps(results)

    return j, 200, {'Content-Type': 'application/json'}


# (e.2) get accommodation by ID
@app.route('/airbnb/accommodations/<id>', methods=['GET'])
def get_accommodation_by_id(id):

    # create connection
    conn = sqlite3.connect("airbnb.db")

    # create a cursor object
    db = conn.cursor()

    # get all accommodation id
    query_1 = "SELECT id FROM accommodation"
    result_1 = db.execute(query_1).fetchall()
    all_accommodation = []
    for row in result_1:
        all_accommodation.append(row[0])

    # get accommodation information with particular id
    query_2 = """
    SELECT name, type, review_score_value, comment, datetime, rname, reviewer.rid, summary, url
    FROM 'accommodation' 
    join (select accommodation_id, group_concat(type) as type
    from amenities
    group by accommodation_id) t on t.accommodation_id = accommodation.id
    join review on review.accommodation_id = accommodation.id
    join reviewer on review.rid = reviewer.rid
    where accommodation.id = ?
    order by datetime DESC
    """
    result_2 = db.execute(query_2, [id]).fetchall()
    name = []
    amenities = []
    score = []
    reviews = []
    summary = []
    url = []
    for row in result_2:
        name.append(row[0])
        amenities.append(convert(row[1]))
        score.append(row[2])
        reviews.append({
            "Comment": row[3],
            "Datetime": row[4],
            "Review Name": row[5],
            "Reviewer ID": row[6]
        })
        summary.append(row[7])
        url.append(row[8])

    # close connection
    conn.close()

    if int(id) in all_accommodation:

        # store the results in dictionary
        results = {"Accommodation ID": int(id),
                   "Accommodation Name": name[0],
                   "Amenities": amenities[0],
                   "Review Score Value": score[0],
                   "Reviews": reviews,
                   "Summary": summary[0],
                   "URL": url[0]
                   }

        # convert to json format
        j = json.dumps(results)

        return j, 200, {'Content-Type': 'application/json'}

    else:
        return jsonify({"Reasons": [
            {'Message': 'Accommodation not found'}
        ]}), 404


def convert(list):
    return list.split(',')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)