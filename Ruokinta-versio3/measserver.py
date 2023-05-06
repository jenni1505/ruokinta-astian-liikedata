import json
from flask import Flask, render_template, request, Response
from flask_socketio import SocketIO, emit
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Lista mittauksia varten

measurements = []


# Näytä mittaukset Google Chart -kaavion avulla
@app.route('/')
def get_line():
    title = 'Ruokinta-astian aktiivisuus'
    return render_template('index.html', title=title)


@app.route('/nippeli')
def nippeli():
    return render_template('nippeli.html')

# Otetaan vastaan HTTP POSTilla lähetty mittaus ja laitetaan se listaan
@app.route('/uusimittaus', methods=['POST'])
def new_meas():
    # luetaan data viestistä ja deserialisoidaan JSON-data
    m = request.get_json(force=True)
    # muutetaan mittaus Google Chartille sopivaan muotoon (sanakirja -> lista)
    mg = [m['alfa'], m['x'], m['y']] #m['z']]
    # laitetaan listamuotoinen mittaus taulukkoon
    measurements.append(mg)
    s = json.dumps(measurements)
    socketio.emit('my_response', {'result': s})
    # palautetaan vastaanotettu tieto
    return json.dumps(m, indent=True)
    

@app.route('/stored')
def get_data():
    title = 'Ruokinta-astian aktiivisuus'
    recent_measurements = measurements[-20:] # only pass the most recent 20 measurements
    return render_template('stored.html', title=title, measurements=recent_measurements)

    

if __name__ == '__main__':
   app.run(debug = True)
   socketio.run(app)
   
