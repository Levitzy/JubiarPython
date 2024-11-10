import logging
from webhook import app

# Suppress Flask's request logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
