from app.main import app
import os
import threading

if __name__ == '__main__':
    # threading.Thread(target=os.system, args=("rasa run --enable-api", )).start()
    app.run(host='0.0.0.0', port='5000', debug=True)
