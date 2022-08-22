
import cgi
import os

from Cheese.cheeseController import CheeseController as cc
from Cheese.cheeseRepository import CheeseRepository as cr
from Cheese.resourceManager import ResMan

from src.repositories.videosRepository import VideosRepository

#@controller /upload;
class UploadController(cc):

    #@post /videos;
    @staticmethod
    def getEmpty(server, path, auth):
        UploadController.deal_post_data(server)

        return cc.createResponse("<script>window.location='/'</script>")

    #@get /load;
    @staticmethod
    def load(server, path, auth):
        index = 0
        cr.disableAutocommit()
        for root, dirs, files in os.walk(ResMan.web("files")):
            for file in files:
                if (file == ".gitkeep"): continue

                if (not VideosRepository.fileExists(file)):
                    UploadController.saveNewFile(file, index)
                    index += 1
        cr.commit()
        cr.enableAutocommit()

        return cc.createResponse({"STATUS": f"{index} files has been updated"})

    # METHODS

    @staticmethod
    def deal_post_data(server):
        ctype, pdict = cgi.parse_header(server.headers['Content-Type'])
        pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
        pdict['CONTENT-LENGTH'] = int(server.headers['Content-Length'])
        if ctype == 'multipart/form-data':
            form = cgi.FieldStorage( fp=server.rfile, headers=server.headers, environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':server.headers['Content-Type'], })
            try:
                cr.disableAutocommit()
                index = 0
                if isinstance(form["file"], list):
                    for record in form["file"]:
                        open(ResMan.web("files", record.filename), "wb").write(record.file.read())
                        UploadController.saveNewFile(record.filename, index)
                        index += 1
                else:
                    open(ResMan.web("files", form["file"].filename), "wb").write(form["file"].file.read())
                    UploadController.saveNewFile(form["file"].filename, index)
                cr.commit()
                cr.enableAutocommit()
            except IOError:
                cr.enableAutocommit()
                return (False, "Can't create file to write, do you have permission to write?")
        return (True, "Files uploaded")

    @staticmethod
    def saveNewFile(name, index):
        filesModel = VideosRepository.model(index)
        filesModel.setAttrs(
            name=name,
            show_name="",
            series="",
            episode=0,
            description=""
        )
        VideosRepository.save(filesModel)