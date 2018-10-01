from __future__ import print_function
import datetime
import requests
import tornado.ioloop
import tornado.httpserver
import tornado.web
import json
import pprint
import mlbgame
import re
import Settings

class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/standings", StandingsHandler),
            (r"/scores", GamesHandler)
        ]
        settings = {
            "template_path": Settings.TEMPLATE_PATH,
            "static_path": Settings.STATIC_PATH,
        }
        tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('index.html')

class StandingsHandler(tornado.web.RequestHandler):

    def get(self):
        r = requests.get('https://erikberg.com/mlb/standings.json')

        standings_dt = "Error Loading Standings Data"

        standings_dt = json.loads(r.text)

        if r.status_code is 200:
            standings_dt = json.dumps(r.text)
            self.write(standings_dt)
            self.finish()

class GamesHandler(tornado.web.RequestHandler):

    def get(self, today = datetime.datetime.today()):
        gm_dt = {}
        day = mlbgame.day(today.year, today.month, today.day)

        for game in day:
            items = game.__dict__.items()
            gm_dt.update({game.game_id: {}})

            for k, v in items:
                if isinstance(v, (datetime.datetime)):
                    v = v.isoformat()

                gm_dt[game.game_id].update({k: v})

        pprint.pprint(gm_dt)

        self.write(gm_dt)
        self.finish()


def main():
    applicaton = Application()
    http_server = tornado.httpserver.HTTPServer(applicaton)
    http_server.listen(8080)

    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
