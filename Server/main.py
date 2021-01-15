# -*- coding: utf-8 -*-
from interface import app, manager, db
from flask_script import Server
## web server script
manager.add_command("run_server", Server(host='0.0.0.0', port=app.config['SERVERPORT'], use_debugger=True, use_reloader=True))





def main():
    app.run(host="0.0.0.0", debug=True)
    db.create_all()



if __name__ == "__main__":
    try:
        import sys
        sys.exit(main())
    except Exception as e:
        import traceback
        traceback.print_exc()
