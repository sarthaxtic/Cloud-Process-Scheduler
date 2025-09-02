import os
from flask import Flask, request, jsonify, render_template, url_for, redirect
from flask_cors import CORS
from fcfs import fcfs
from preemtive_priority import preemptive_priority
from preemtive_sjf import preemptive_sjf
from priority import priority
from round_robin import round_robin
from sjf import sjf
from suggestions import suggest_best_algorithm

# Calculate absolute base path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

# Configure Flask app with absolute paths
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'frontend', 'templates'),
    static_folder=os.path.join(BASE_DIR, 'frontend', 'static')
)

CORS(app)

# In-memory process list
processes = []

# ----- HTML Page Routes -----

@app.route('/')
def home():
    return render_template('mainWindow.html')

@app.route('/predict')
def predict_page():
    return render_template('Recommended.html')

@app.route('/exit')
def exit_app():
    return "Goodbye! You may close the tab."

@app.route('/algorithm')
def algorithm():
    selected = request.args.get('selected')
    if selected == 'fcfs':
        return redirect(url_for('fcfs_page'))
    elif selected == 'sjf':
        return redirect(url_for('sjf_page'))
    elif selected == 'priority':
        return redirect(url_for('priority_page'))
    elif selected == 'preemptivepriority':
        return redirect(url_for('preemptive_priority_page'))
    elif selected == 'preemptivesjf':
        return redirect(url_for('preemptive_sjf_page'))
    elif selected == 'rr':
        return redirect(url_for('rr_page'))
    elif selected == 'recommended':
        return redirect(url_for('recommended_page'))
    else:
        return "Unknown algorithm selected", 400

@app.route('/fcfs')
def fcfs_page():
    return render_template('fcfs.html')

@app.route('/sjf')
def sjf_page():
    return render_template('SJF.html')

@app.route('/priority')
def priority_page():
    return render_template('priority.html')

@app.route('/preemptivepriority')
def preemptive_priority_page():
    return render_template('preemptivepriority.html')

@app.route('/preemptivesjf')
def preemptive_sjf_page():
    return render_template('preemptiveSJF.html')

@app.route('/rr')
def rr_page():
    return render_template('RR.html')

@app.route('/recommended')
def recommended_page():
    return render_template('Recommended.html')

# ----- API Routes -----

@app.route('/api/<algo>', methods=['POST'])
def schedule(algo):
    data = request.get_json()
    processes = data.get('processes', [])
    quantum = data.get('quantum', None)

    if algo == 'fcfs':
        return jsonify(fcfs(processes))
    elif algo == 'sjf':
        return jsonify(sjf(processes))
    elif algo == 'preemptive-sjf':
        return jsonify(preemptive_sjf(processes))
    elif algo == 'priority':
        return jsonify(priority(processes))
    elif algo == 'preemptive-priority':
        return jsonify(preemptive_priority(processes))
    elif algo == 'round-robin':
        if quantum is None:
            return jsonify({"error": "Quantum required for Round Robin"}), 400
        return jsonify(round_robin(processes, quantum))
    else:
        return jsonify({"error": "Unsupported algorithm"}), 400

@app.route('/get_processes')
def get_processes():
    return jsonify(processes)

@app.route('/add_process', methods=['POST'])
def add_process():
    try:
        arrival = int(request.form['arrival_time'])
        burst = int(request.form['burst_time'])
        priority = int(request.form.get('priority', 0))

        process = {
            "pid": len(processes) + 1,
            "arrival_time": arrival,
            "burst_time": burst,
            "priority": priority
        }
        processes.append(process)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/reset', methods=['POST'])
def reset():
    processes.clear()
    return jsonify({"message": "All processes cleared"})

@app.route('/predict-algorithm', methods=['POST'])
def predict_algorithm():
    data = request.get_json()
    proc_list = data.get('processes', [])
    quantum = data.get('quantum')
    algo, reason = suggest_best_algorithm(proc_list, quantum)
    return jsonify({
        "algorithm": algo.upper(),
        "reason": reason
    })

if __name__ == '__main__':
    app.run(debug=True)
