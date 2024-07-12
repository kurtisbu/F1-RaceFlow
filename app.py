from flask import Flask, render_template, request, jsonify
import plotly.graph_objects as go
import plotly
import json
from config import YEARS, SESSIONS
from utils import get_session_data, get_driver_names, get_telemetry_data, get_available_grand_prix

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', years=YEARS, sessions=SESSIONS)

@app.route('/get_grand_prix', methods=['POST'])
def get_grand_prix():
    data = request.json
    year = int(data['year'])
    grand_prix_list = get_available_grand_prix(year)
    return jsonify(grand_prix_list)

@app.route('/get_drivers', methods=['POST'])
def get_drivers():
    data = request.json
    year = int(data['year'])
    grand_prix = data['grand_prix']
    session = data['session']
    
    session_data = get_session_data(year, grand_prix, session)
    driver_names = get_driver_names(session_data)
    
    return jsonify(driver_names)

@app.route('/race', methods=['POST'])
def race():
    year = int(request.form['year'])
    grand_prix = request.form['grand_prix']
    session = request.form['session']
    selected_driver = request.form['driver']
    
    session_data = get_session_data(year, grand_prix, session)
    
    laps = session_data.laps.pick_driver(selected_driver)
    telemetry = laps.pick_fastest().get_telemetry()

    # Convert telemetry data to lists for plotly
    telemetry_x = telemetry['X'].tolist()
    telemetry_y = telemetry['Y'].tolist()

    # Plot track layout with telemetry data
    track_layout = go.Figure()
    track_layout.add_trace(go.Scatter(x=telemetry_x, y=telemetry_y, mode='lines', name=selected_driver))
    track_layout.update_layout(title=f'{grand_prix} Track Layout', xaxis_title='X', yaxis_title='Y')

    # Plot lap times
    lap_numbers = laps['LapNumber']
    lap_times = laps['LapTime'].apply(lambda x: x.total_seconds())

    lap_time_plot = go.Figure()
    lap_time_plot.add_trace(go.Scatter(x=lap_numbers, y=lap_times, mode='lines+markers', name=selected_driver))
    lap_time_plot.update_layout(title=f'{grand_prix} {session} {year}', xaxis_title='Lap Number', yaxis_title='Lap Time (seconds)')

    track_layout_json = json.dumps(track_layout, cls=plotly.utils.PlotlyJSONEncoder)
    lap_time_plot_json = json.dumps(lap_time_plot, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('race.html', track_layout_json=track_layout_json, lap_time_plot_json=lap_time_plot_json, year=year, grand_prix=grand_prix, session=session, driver=selected_driver)

@app.route('/lap_info', methods=['POST'])
def lap_info():
    year = int(request.form['year'])
    grand_prix = request.form['grand_prix']
    session = request.form['session']
    selected_driver = request.form['driver']
    lap_number = int(request.form['lap_number'])

    session_data = get_session_data(year, grand_prix, session)
    telemetry_data = get_telemetry_data(session_data, selected_driver, lap_number)
    
    return jsonify(telemetry_data)

if __name__ == '__main__':
    app.run(debug=True)
