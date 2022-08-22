
import os

from Cheese.cheeseController import CheeseController as cc
from Cheese.resourceManager import ResMan
from Cheese.httpClientErrors import *

from src.repositories.videosRepository import VideosRepository

#@controller /video;
class VideoController(cc):

    #@get /remove;
    @staticmethod
    def remove(server, path, auth):
        args = cc.getArgs(path)
        cc.checkJson(["id"], args)    

        video =  VideosRepository.find(args["id"])
        VideosRepository.delete(video)

        if (os.path.exists(ResMan.web("files", video.name))):
            os.remove(ResMan.web("files", video.name))

        return cc.createResponse({"STATUS": "OK"})

    #@get /getByName;
    @staticmethod
    def getByName(server, path, auth):
        args = cc.getArgs(path)
        cc.checkJson(["name"], args)

        video = VideosRepository.findOneBy("name", args["name"])

        return cc.createResponse({"VIDEO": video.toJson()})

    #@post /update;
    @staticmethod
    def update(server, path, auth):
        args = cc.readArgs(server)
        cc.checkJson(["ID", "NAME", "SHOW_NAME", "SERIES", "EPISODE", "DESCRIPTION"], args)
 
        if (not args["NAME"].endswith(".mp4")):
            args["NAME"] += ".mp4"

        video = VideosRepository.find(args["ID"])

        if (video.name != args["NAME"]):
            if (os.path.exists(ResMan.web("files", args["NAME"]))):
                raise Conflict("VIdeo with this name already exists")

            os.rename(ResMan.web("files", video.name), ResMan.web("files", args["NAME"]))

        video.setAttrs(
            name=args["NAME"],
            show_name=args["SHOW_NAME"],
            series=args["SERIES"],
            episode=args["EPISODE"],
            description=args["DESCRIPTION"]
        )
        VideosRepository.update(video)

        return cc.createResponse({"STATUS": "OK"})

    #@get /getAll;
    @staticmethod
    def getAll(server, path, auth):
        videos = VideosRepository.findAllOrderByEpisodeAndName()

        shows = {}
        for video in videos:
            if (video.show_name not in shows.keys()):
                shows[video.show_name] = {}

            if (video.series not in shows[video.show_name].keys()):
                shows[video.show_name][video.series] = []

            shows[video.show_name][video.series].append(video.toJson())

        return cc.createResponse({"SHOWS": shows})

    #@get /neighbors;
    @staticmethod
    def neighbors(server, path, auth):
        args = cc.getArgs(path)
        cc.checkJson(["id"], args)

        resp = {
            "BEFORE": None,
            "AFTER": None
        }

        video = VideosRepository.find(args["id"])
        if (video.episode != None and video.episode != 0):
            before = VideosRepository.findByShowAndSeriesAndEpisode(video.show_name, video.series, video.episode-1)
            after = VideosRepository.findByShowAndSeriesAndEpisode(video.show_name, video.series, video.episode+1)

            if (before != None):
                resp["BEFORE"] = before.toJson()
            if (after != None):
                resp["AFTER"] = after.toJson()

        return cc.createResponse({"NEIGHBORS": resp})

