# Program to control light using webpage

from flask import Flask, render_template
import time
import datetime
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

led = 15
GPIO.setup(led, GPIO.OUT)

app = Flask(__name__)

@app.route('/')
def hello():
    GPIO.output(led, True)
    return render_template('pro6_web.html', status='OFF', time='')

@app.route('/ledon')
def ledOn():
    now = datetime.datetime.now()
    t = now.strftime('%Y - %m - %d %H : %M')
    d = {'status': 'ON', 'time': t}
    GPIO.output(led, False)
    return render_template('pro6_web.html', **d)

if __name__ == '__main__':
    app.run(debug=True, host='192.168.0.18', port=5000)

# Cleanup GPIO pins when the program exits
try:
    while True:
        time.sleep(3)
except KeyboardInterrupt:
    GPIO.cleanup()
