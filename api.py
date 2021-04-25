import datetime
import json

from flask import Flask
from flask import jsonify
from flask_cors import cross_origin
from flask_pymongo import PyMongo


def getJSON(filePathAndName):
    with open(filePathAndName, 'r') as fp:
        return json.load(fp)


private = getJSON('./private.json')

IP = private.get("IP")
MongoDBPass = private.get("MongoPass")

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'HightLimitMod'
app.config['MONGO_URI'] = MongoDBPass
mongo = PyMongo(app)


@app.route('/HeightLimitMod/BedWars', methods=['GET'])
@cross_origin()
def get_all_maps():
    Name = mongo.db.BedWars
    output = []
    for s in Name.find():
        output.append(
            {'MapName': s['MapName'], "Limit": s["Limit"], "Mode": s["Mode"]}
        )
    return jsonify(output)


@app.route('/HeightLimitMod/HeightLimitApp', methods=['GET'])
@cross_origin()
def get_HLA():
    Name = mongo.db.HeightLimitApp
    v = Name.find_one({'_id': 1})
    output = {'version': v['version'], "announcement": v["announcement"]}
    return jsonify(output)


@app.route('/HeightLimitMod/BedWars/data', methods=['GET'])
@cross_origin()
def get_data():
    a_file = open("data.json", "r")
    json_object = json.load(a_file)
    a_file.close()
    json_object["server_time"]['timestamp'] = datetime.datetime.now().timestamp()
    json_object["server_time"]['date'] = f"{datetime.date.today()}"
    json_object["server_time"][
        "time"] = f"{datetime.datetime.now().time().hour}:{datetime.datetime.now().time().minute}:{datetime.datetime.now().time().second}"
    return jsonify(json_object)


@app.route(f'/HeightLimitMod/BedWars/8team/<MapName>', methods=['GET'])
@cross_origin()
def get_one_8team_map(MapName):
    MapName = MapName
    Name = mongo.db.BedWars
    s = Name.find_one({'MapName': f"{MapName}", 'Mode': 'solo/doubles'})
    if s:
        a_file = open("data.json", "r")
        json_object = json.load(a_file)
        a_file.close()

        # Total
        if f"{MapName}" in json_object["solo/doubles"]["total"]:
            with open("data.json", "r+") as file:
                data = json.load(file)
                data["solo/doubles"]["total"].update({f'{MapName}': data['solo/doubles']["total"][MapName] + 1})
                data["solo/doubles"]["total"].update(
                    {f'TotalCalls': data['solo/doubles']["total"]["TotalCalls"] + 1})
                file.seek(0)
                json.dump(data, file, indent=4)
        else:
            with open("data.json", "r+") as file:
                data = json.load(file)
                data["solo/doubles"]["total"].update(
                    {f'TotalCalls': data['solo/doubles']["total"]["TotalCalls"] + 1})
                data["solo/doubles"]["total"].update({f'{MapName}': 1})

                file.seek(0)
                json.dump(data, file, indent=4)
        a_file = open("data.json", "r")
        json_object = json.load(a_file)
        a_file.close()
        # Today
        if f"{datetime.date.today()}" in json_object["solo/doubles"]:
            with open("data.json", "r+") as file:
                data = json.load(file)
                data["solo/doubles"][f"{datetime.date.today()}"]["total"].update(
                    {f'TotalCalls': data['solo/doubles'][f"{datetime.date.today()}"]["total"]["TotalCalls"] + 1})
                file.seek(0)
                json.dump(data, file, indent=4)

        else:
            with open("data.json", "r+") as file:
                data = json.load(file)
                data["solo/doubles"].update({f'{datetime.date.today()}': {"total": {"TotalCalls": 1}}})
                file.seek(0)
                json.dump(data, file, indent=4)

        a_file = open("data.json", "r")
        json_object = json.load(a_file)
        a_file.close()
        if f"{MapName}" in json_object["solo/doubles"][f"{datetime.date.today()}"]["total"]:
            with open("data.json", "r+") as file:
                data = json.load(file)
                data["solo/doubles"][f'{datetime.date.today()}']["total"].update(
                    {f'{MapName}': data['solo/doubles'][f'{datetime.date.today()}']["total"][MapName] + 1})
                file.seek(0)
                json.dump(data, file, indent=4)
        else:
            with open("data.json", "r+") as file:
                data = json.load(file)
                data["solo/doubles"][f'{datetime.date.today()}']["total"].update({f'{MapName}': 1})
                file.seek(0)
                json.dump(data, file, indent=4)

        # Hour
        a_file = open("data.json", "r")
        json_object = json.load(a_file)
        a_file.close()
        if f"{datetime.datetime.now().hour}" in json_object["solo/doubles"][f"{datetime.date.today()}"]:
            with open("data.json", "r+") as file:
                data = json.load(file)
                data["solo/doubles"][f"{datetime.date.today()}"][f"{datetime.datetime.now().hour}"].update(
                    {f'TotalCalls': data['solo/doubles'][f"{datetime.date.today()}"][f"{datetime.datetime.now().hour}"][
                                        "TotalCalls"] + 1})
                file.seek(0)
                json.dump(data, file, indent=4)

        else:
            with open("data.json", "r+") as file:
                data = json.load(file)
                data["solo/doubles"][f"{datetime.date.today()}"].update(
                    {f'{datetime.datetime.now().hour}': {"TotalCalls": 1}})
                file.seek(0)
                json.dump(data, file, indent=4)
        a_file = open("data.json", "r")
        json_object = json.load(a_file)
        a_file.close()
        if f"{MapName}" in json_object["solo/doubles"][f"{datetime.date.today()}"][f"{datetime.datetime.now().hour}"]:
            with open("data.json", "r+") as file:
                data = json.load(file)
                data["solo/doubles"][f'{datetime.date.today()}'][f"{datetime.datetime.now().hour}"].update(
                    {f'{MapName}': data['solo/doubles'][f'{datetime.date.today()}'][f"{datetime.datetime.now().hour}"][
                                       MapName] + 1})
                file.seek(0)
                json.dump(data, file, indent=4)
        else:
            with open("data.json", "r+") as file:
                data = json.load(file)
                data["solo/doubles"][f'{datetime.date.today()}'][f"{datetime.datetime.now().hour}"].update(
                    {f'{MapName}': 1})
                file.seek(0)
                json.dump(data, file, indent=4)
        output = {'MapName': s['MapName'], "Limit": s["Limit"], "Mode": s["Mode"]}
        return jsonify(output)
    else:
        output = "Invalid map name"
        return jsonify({'error': output})


@app.route(f'/HeightLimitMod/BedWars/4team/<MapName>', methods=['GET'])
@cross_origin()
def get_one_4_team_map(MapName):
    MapName = MapName
    Name = mongo.db.BedWars
    s = Name.find_one({'MapName': f"{MapName}", 'Mode': '3v3v3v3/4v4v4v4'})
    if s:
        a_file = open("data.json", "r")
        json_object = json.load(a_file)
        a_file.close()

        # Total
        if f"{MapName}" in json_object["3v3v3v3/4v4v4v4"]["total"]:
            with open("data.json", "r+") as file:
                data = json.load(file)
                data["3v3v3v3/4v4v4v4"]["total"].update({f'{MapName}': data['3v3v3v3/4v4v4v4']["total"][MapName] + 1})
                data["3v3v3v3/4v4v4v4"]["total"].update(
                    {f'TotalCalls': data['3v3v3v3/4v4v4v4']["total"]["TotalCalls"] + 1})
                file.seek(0)
                json.dump(data, file, indent=4)
        else:
            with open("data.json", "r+") as file:
                data = json.load(file)
                data["3v3v3v3/4v4v4v4"]["total"].update(
                    {f'TotalCalls': data['3v3v3v3/4v4v4v4']["total"]["TotalCalls"] + 1})
                data["3v3v3v3/4v4v4v4"]["total"].update({f'{MapName}': 1})

                file.seek(0)
                json.dump(data, file, indent=4)
        a_file = open("data.json", "r")
        json_object = json.load(a_file)
        a_file.close()
        # Today
        if f"{datetime.date.today()}" in json_object["3v3v3v3/4v4v4v4"]:
            with open("data.json", "r+") as file:
                data = json.load(file)
                data["3v3v3v3/4v4v4v4"][f"{datetime.date.today()}"]["total"].update(
                    {f'TotalCalls': data['3v3v3v3/4v4v4v4'][f"{datetime.date.today()}"]["total"]["TotalCalls"] + 1})
                file.seek(0)
                json.dump(data, file, indent=4)

        else:
            with open("data.json", "r+") as file:
                data = json.load(file)
                data["3v3v3v3/4v4v4v4"].update({f'{datetime.date.today()}': {'total': {"TotalCalls": 1}}})
                file.seek(0)
                json.dump(data, file, indent=4)
        a_file = open("data.json", "r")
        json_object = json.load(a_file)
        a_file.close()
        if f"{MapName}" in json_object["3v3v3v3/4v4v4v4"][f"{datetime.date.today()}"]["total"]:
            with open("data.json", "r+") as file:
                data = json.load(file)
                data["3v3v3v3/4v4v4v4"][f'{datetime.date.today()}']["total"].update(
                    {f'{MapName}': data['3v3v3v3/4v4v4v4'][f'{datetime.date.today()}']['total'][MapName] + 1})
                file.seek(0)
                json.dump(data, file, indent=4)
        else:
            with open("data.json", "r+") as file:
                data = json.load(file)
                data["3v3v3v3/4v4v4v4"][f'{datetime.date.today()}']['total'].update({f'{MapName}': 1})
                file.seek(0)
                json.dump(data, file, indent=4)

        # Hour
        a_file = open("data.json", "r")
        json_object = json.load(a_file)
        a_file.close()
        if f"{datetime.datetime.now().hour}" in json_object["3v3v3v3/4v4v4v4"][f"{datetime.date.today()}"]:
            with open("data.json", "r+") as file:
                data = json.load(file)
                data["3v3v3v3/4v4v4v4"][f"{datetime.date.today()}"][f"{datetime.datetime.now().hour}"].update(
                    {f'TotalCalls':
                         data['3v3v3v3/4v4v4v4'][f"{datetime.date.today()}"][f"{datetime.datetime.now().hour}"][
                             "TotalCalls"] + 1})
                file.seek(0)
                json.dump(data, file, indent=4)

        else:
            with open("data.json", "r+") as file:
                data = json.load(file)
                data["3v3v3v3/4v4v4v4"][f"{datetime.date.today()}"].update(
                    {f'{datetime.datetime.now().hour}': {"TotalCalls": 1}})
                file.seek(0)
                json.dump(data, file, indent=4)
        a_file = open("data.json", "r")
        json_object = json.load(a_file)
        a_file.close()
        if f"{MapName}" in json_object["3v3v3v3/4v4v4v4"][f"{datetime.date.today()}"][
            f"{datetime.datetime.now().hour}"]:
            with open("data.json", "r+") as file:
                data = json.load(file)
                data["3v3v3v3/4v4v4v4"][f'{datetime.date.today()}'][f"{datetime.datetime.now().hour}"].update(
                    {f'{MapName}':
                         data['3v3v3v3/4v4v4v4'][f'{datetime.date.today()}'][f"{datetime.datetime.now().hour}"][
                             MapName] + 1})
                file.seek(0)
                json.dump(data, file, indent=4)
        else:
            with open("data.json", "r+") as file:
                data = json.load(file)
                data["3v3v3v3/4v4v4v4"][f'{datetime.date.today()}'][f"{datetime.datetime.now().hour}"].update(
                    {f'{MapName}': 1})
                file.seek(0)
                json.dump(data, file, indent=4)
        output = {'MapName': s['MapName'], "Limit": s["Limit"], "Mode": s["Mode"]}
        return jsonify(output)
    else:
        output = "Invalid map name"
        return jsonify({'error': output})


@app.errorhandler(404)
@cross_origin()
def non_exist_route(error):
    return jsonify({"success": False,
                    "cause": 404}), 404


@app.route('/HeightLimitMod/version', methods=['GET'])
@cross_origin()
def get_version():
    version = mongo.db.Version
    v = version.find_one({'_id': 1})
    output = {'Version': v['Version'], "Info": v["UpdateInfo"]}
    return jsonify(output)


if __name__ == '__main__':
    app.run(debug=True, host="localhost", port=80)
