import requests
import tornado.ioloop
import tornado.httpserver
import tornado.web
import json
import pprint
import re
import Settings

class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/standings", StandingsHandler)
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

        print(r.status_code)
        standings_dt = "Error Loading Standings Data"

        standings_dt = json.loads(r.text)

        if r.status_code is 200:
            standings_dt = json.dumps(r.text)
            self.write(standings_dt)
            self.finish()

def main():
    applicaton = Application()
    http_server = tornado.httpserver.HTTPServer(applicaton)
    http_server.listen(8888)

    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
