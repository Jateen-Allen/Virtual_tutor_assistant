from flask import Flask, render_template, jsonify, request
import subprocess
import signal
import os

app = Flask(__name__)

# Global variable to store the current process
current_process = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    global current_process
    
    if current_process:
        return jsonify({'status': 'error', 'message': 'Process already running'})
    
    mode = request.json.get('mode', 'screen')
    try:
        # Start the Gemini script as a subprocess
        current_process = subprocess.Popen(['python', 'gemini.py', '--mode', mode], 
                                        cwd=os.path.dirname(os.path.abspath(__file__)))
        return jsonify({'status': 'success', 'message': f'Started with mode: {mode}'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/stop', methods=['POST'])
def stop():
    global current_process
    
    if current_process:
        try:
            # Send SIGTERM signal to the process group
            os.killpg(os.getpgid(current_process.pid), signal.SIGTERM)
            current_process = None
            return jsonify({'status': 'success', 'message': 'Stopped successfully'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})
    return jsonify({'status': 'error', 'message': 'No process running'})

if __name__ == '__main__':
    app.run(debug=True) 