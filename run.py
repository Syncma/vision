from bottle import run
from vision.app import init_app

app = application = init_app()

if __name__ == '__main__':

    run(app, debug=True, reloader=True, port=1127)
