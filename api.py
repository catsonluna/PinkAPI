import datetime
import json

from flask import Flask, request, render_template
from flask import jsonify
from flask_cors import cross_origin
from flask_pymongo import PyMongo
from discord_webhook import DiscordWebhook, DiscordEmbed
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


def getJSON(filePathAndName):
    with open(filePathAndName, 'r') as fp:
        return json.load(fp)


private = getJSON('./private.json')

IP = private.get("IP")
MongoDBPass = private.get("MongoPass")
MongoDBPass2 = private.get("MongoPass2")

HLMWebhook = private.get("HLMWebhook")
PSWebhook = private.get("PSWebhook")

app = Flask(__name__)
mongo1 = PyMongo(app, uri=f'{MongoDBPass}/HightLimitMod')
mongo2 = PyMongo(app, uri=f'{MongoDBPass2}')

limiter = Limiter(app, key_func=get_remote_address)


@app.route('/HeightLimitMod/BedWars', methods=['GET'])
@cross_origin()
def get_all_maps():
    Name = mongo1.db.BedWars
    output = []
    for s in Name.find():
        output.append(
            {'MapName': s['MapName'], "Limit": s["Limit"], "Mode": s["Mode"]}
        )
    return jsonify(output)


@app.route('/HeightLimitMod/HeightLimitApp', methods=['GET'])
@cross_origin()
def get_HLA_version():
    Name = mongo1.db.HeightLimitApp
    v = Name.find_one({'_id': 1})
    output = {'version': v['version'], "announcement": v["announcement"]}
    return jsonify(output)


@app.route(f'/HeightLimitMod/BedWars/8team/<MapName>', methods=['GET'])
@cross_origin()
@limiter.limit("10/minute")
def get_one_8team_map(MapName):
    MapName = MapName
    Name = mongo1.db.BedWars
    s = Name.find_one({'MapName': f"{MapName}", 'Mode': 'solo/doubles'})
    try:
        if s:
            webhook = DiscordWebhook(
                url=f'{HLMWebhook}',
                username="PinkAPI")
            embed = DiscordEmbed(title=MapName, description=f"{MapName} was called successfully", color='02f418')
            embed.add_embed_field(name="Limit: ", value=s['Limit'], inline=False)
            embed.add_embed_field(name="Mode: ", value=s['Mode'], inline=False)
            embed.set_timestamp()
            webhook.add_embed(embed)
            webhook.execute()
            output = {'MapName': s['MapName'], "Limit": s["Limit"], "Mode": s["Mode"]}
            return jsonify(output)
        else:
            output = "Invalid map name"
            return jsonify({'error': output})
    except:
        webhook = DiscordWebhook(
            url=f'{HLMWebhook}',
            username="PinkAPI")
        embed = DiscordEmbed(title=MapName, description=f"there was an error calling {MapName}", color='fd1916')
        embed.add_embed_field(name="Mode", value="solo/doubles", inline=False)
        embed.set_timestamp()
        webhook.content = '<@324553306682818561>'
        webhook.add_embed(embed)
        webhook.execute()
    return jsonify({'error': f"An error occurred {MapName}"})


@app.route(f'/HeightLimitMod/BedWars/4team/<MapName>', methods=['GET'])
@cross_origin()
@limiter.limit("10/minute")
def get_one_4_team_map(MapName):
    MapName = MapName
    Name = mongo1.db.BedWars
    s = Name.find_one({'MapName': f"{MapName}", 'Mode': '3v3v3v3/4v4v4v4'})
    try:
        if s:
            webhook = DiscordWebhook(
                url=f'{HLMWebhook}',
                username="PinkAPI")
            embed = DiscordEmbed(title=MapName, description=f"{MapName} was called successfully", color='02f418')
            embed.add_embed_field(name="Limit: ", value=s['Limit'], inline=False)
            embed.add_embed_field(name="Mode: ", value=s['Mode'], inline=False)
            embed.set_timestamp()
            webhook.add_embed(embed)
            webhook.execute()
            output = {'MapName': s['MapName'], "Limit": s["Limit"], "Mode": s["Mode"]}
            return jsonify(output)
        else:
            output = "Invalid map name"
            return jsonify({'error': output})
    except:
        webhook = DiscordWebhook(
            url=f'{HLMWebhook}',
            username="PinkAPI")
        embed = DiscordEmbed(title=MapName, description=f"there was an error calling {MapName}", color='fd1916')
        embed.add_embed_field(name="Mode", value="3v3v3v3/4v4v4v4", inline=False)
        embed.set_timestamp()
        webhook.content = '<@324553306682818561>'
        webhook.add_embed(embed)
        webhook.execute()
    return jsonify({'error': f"An error occurred {MapName}"})


@app.route('/HeightLimitMod/version', methods=['GET'])
@cross_origin()
def get_HLM_version():
    version = mongo1.db.Version
    v = version.find_one({'_id': 1})
    output = {'Version': v['Version'], "Info": v["UpdateInfo"]}
    return jsonify(output)


@app.errorhandler(404)
@cross_origin()
def non_exist_route():
    return jsonify({"success": False,
                    "cause": 404}), 404


@app.errorhandler(429)
def ratelimit_handler():
    return jsonify({"success": False,
                    "cause": 429}), 429


@app.route('/PinkStats/version', methods=['GET'])
@cross_origin()
def get_PS_version():
    version = mongo2.db.Version
    v = version.find_one({'_id': 1})
    output = {'Version': v['Version'], "Info": v["UpdateInfo"]}
    return jsonify(output)


@app.route('/PinkStats/auth', methods=['GET'])
@cross_origin()
def get_PS_auths():
    API_KEY_USER = mongo2.db.api_keys
    USER = mongo2.db.users
    try:
        key = request.values.get("key")
    except:
        key = None

    try:
        uuid = request.values.get("uuid")
    except:
        uuid = None
    if key is None:
        output = {"Key Found": False, "UUID Found": False, "error": "no key was provided"}
        return jsonify(output), 401

    if uuid is None:
        output = {"Key Found": False, "UUID Found": False, "error": "no uuid was provided"}
        return jsonify(output), 401

    s = API_KEY_USER.find_one({'api_key': key})
    if s:
        if not s['Banned']:
            user = USER.find_one({'uuid': s['uuid']})
            print(user)
            if s['uuid'] == uuid:
                output = {"Key Found": True, "UUID Found": True}
                return jsonify(output)
            else:
                output = {"Key Found": False, "UUID Found": False, "error": "This api key does not belong to this uuid"}
                return jsonify(output)
        else:
            return ({"Key Found": False, "UUID Found": False, "error": "You have been banned",
                     "reason": s['Ban Reason']}), 403
    else:
        output = {"Key Found": False, "UUID Found": False, "error": "Your api key is invalid"}
        return jsonify(output), 401


@app.route('/PinkStats/info', methods=['GET', 'POST'])
def get_PS_locraw():
    if request.method == 'GET':
        return {"error": "You cant use GET here"}
    API_KEY_USER = mongo2.db.api_keys
    USER = mongo2.db.users
    try:
        key = request.values.get("key")
    except:
        key = None

    try:
        uuid = request.values.get("uuid")
    except:
        uuid = None
    if key is None:
        return jsonify({"error": "no key was provided"}), 401

    if uuid is None:
        return jsonify({"error": "no uuid was provided"}), 401

    s = API_KEY_USER.find_one({'api_key': key})
    if s:
        user = USER.find_one({'uuid': s['uuid']})
        content = request.get_json()
        if not s['Banned']:
            if "lobby" in content['server'] or "limbo" in content['server']:
                return ({"error": "get out of the lobby"}), 401
            if "mode" in content and "map" in content:
                try:
                    count = user['Overall'][f"{content['gametype']}"][f"{content['mode']}"][f"{content['map']}"] + 1
                    USER.update_one({'uuid': s['uuid']},
                                    {"$set": {
                                        f"Overall.{content['gametype']}.{content['mode']}.{content['map']}": count}})
                except:
                    USER.update_one({'uuid': s['uuid']},
                                    {"$set": {
                                        f"Overall.{content['gametype']}.{content['mode']}.{content['map']}": 1}})
                try:
                    count = user['Overtime'][f"{datetime.date.today()}"]['Total'][f"{content['gametype']}"][
                                f"{content['mode']}"][f"{content['map']}"] + 1
                    USER.update_one({'uuid': s['uuid']},
                                    {"$set": {
                                        f"Overtime.{datetime.date.today()}.Total.{content['gametype']}.{content['mode']}.{content['map']}": count}})
                except:
                    USER.update_one({'uuid': s['uuid']},
                                    {"$set": {
                                        f"Overtime.{datetime.date.today()}.Total.{content['gametype']}.{content['mode']}.{content['map']}": 1}})
                try:
                    count = user['Overtime'][f"{datetime.date.today()}"][f"{datetime.datetime.now().hour}"][
                                f"{content['gametype']}"][f"{content['mode']}"][f"{content['map']}"] + 1
                    USER.update_one({'uuid': s['uuid']},
                                    {"$set": {
                                        f"Overtime.{datetime.date.today()}.{datetime.datetime.now().now()}.{content['gametype']}.{content['mode']}.{content['map']}": count}})
                except:
                    USER.update_one({'uuid': s['uuid']},
                                    {"$set": {
                                        f"Overtime.{datetime.date.today()}.{datetime.datetime.now().hour}.{content['gametype']}.{content['mode']}.{content['map']}": 1}})
                try:
                    webhook = DiscordWebhook(
                        url=f'{PSWebhook}',
                        username="PinkAPI")
                    embed = DiscordEmbed(title="PinkStats",
                                         color='02f418')
                    embed.add_embed_field(name="Gametype: ", value=content['gametype'], inline=False)
                    embed.add_embed_field(name="Mode:", value=content['mode'], inline=False)
                    embed.add_embed_field(name="Map:", value=content['map'], inline=False)
                    embed.add_embed_field(name="UUID:", value=s['uuid'], inline=False)
                    embed.set_timestamp()
                    webhook.add_embed(embed)
                    webhook.execute()
                except:
                    pass
            return {"this": "worked"}
        else:
            return ({"error": "You have been banned", "reason": s['Ban Reason']}), 403
    else:
        return {"error": "invalid api key"}, 401


if __name__ == '__main__':
    app.run(debug=True, host="localhost", port=80)
