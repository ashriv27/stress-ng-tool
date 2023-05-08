from flask import Flask, jsonify, request, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('stress_cpu.html')

@app.route('/stress_cpu', methods=['POST'])
def stress_cpu():
    if request.method == 'POST':
        stress_time = request.form['stress_time']
        cmd = f'stress-ng --cpu 1 --timeout {stress_time}s'
        output = subprocess.check_output(cmd.split(), stderr=subprocess.STDOUT)
        output_lines = output.decode('utf-8').split('\n')
        print(output_lines)
        response = jsonify({'output': output_lines})
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    else:
        return render_template('stress_cpu.html')

@app.route('/check_temp', methods=['POST'])
def check_temp():
    if request.method == 'POST':
        stress_time = request.form.get('stress_time')
        cpu_number = request.form.get('cpu_number')
        cmd = f'stress-ng --cpu {cpu_number} --tz -t {stress_time}s'
        output = subprocess.check_output(cmd.split(), stderr=subprocess.STDOUT)
        output_lines = output.decode('utf-8').split('\n')
        print(output_lines)
        response = jsonify({'output': output_lines})
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    else:
        # Handle GET request
        return render_template('stress_cpu.html')

@app.route('/stress_matrix', methods=['POST'])
def stress_matrix():
    if request.method == 'POST':
        stress_time = request.form.get('stress_time')
        cpu_number = request.form.get('cpu_number')
        cmd = f'stress-ng --matrix {cpu_number} -t {stress_time}s --times'
        output = subprocess.check_output(cmd.split(), stderr=subprocess.STDOUT)
        output_lines = output.decode('utf-8').split('\n')
        print(output_lines)
        response = jsonify({'output': output_lines})
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    else:
        # Handle GET request
        return render_template('stress_cpu.html')

@app.route('/interrupt_load', methods=['POST'])
def interrupt_load():
    if request.method == 'POST':
        if request.form.get('stress_time') is None:
            time = 0
        else:
            time = request.form.get('stress_time')

        frequency = request.form.get('frequency')
        cpu_number = request.form.get('cpu_number')
        cmd = f'stress-ng --timer  {cpu_number} --timer-freq {frequency} -t {time}'
        output = subprocess.check_output(cmd.split(), stderr=subprocess.STDOUT)
        output_lines = output.decode('utf-8').split('\n')
        print(output_lines)
        response = jsonify({'output': output_lines})
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    else:
        # Handle GET request
        return render_template('stress_cpu.html')

@app.route('/iomix_stressor', methods=['POST'])
def iomix_stressor():
    if request.method == 'POST':
        if request.form.get('stress_time') is None:
            time = 0
        else:
            time = request.form.get('stress_time')

        cpu_number = request.form.get('cpu_number')
        cmd = f'stress-ng --iomix  {cpu_number} -t {time} -v'
        output = subprocess.check_output(cmd.split(), stderr=subprocess.STDOUT)
        output_lines = output.decode('utf-8').split('\n')
        print(output_lines)
        response = jsonify({'output': output_lines})
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    else:
        # Handle GET request
        return render_template(request, 'stress_cpu.html')

@app.route('/virtual_memory_stressor', methods=['POST'])
def virtual_memory_stressor():
    if request.method == 'POST':
        if request.form.get('stress_time') is None:
            time = 0
        else:
            time = request.form.get('stress_time')

        vmnumber = request.form.get('vmnumber')
        cpu_number = request.form.get('cpu_number')
        cmd = f'stress-ng --cpu  {cpu_number} --vm {vmnumber} -t {time}'
        output = subprocess.check_output(cmd.split(), stderr=subprocess.STDOUT)
        output_lines = output.decode('utf-8').split('\n')
        print(output_lines)
        response = jsonify({'output': output_lines})
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    else:
        # Handle GET request
        return render_template(request, 'stress_cpu.html')

@app.route('/check_status', methods=['GET'])
def check_status():
    if request.method == 'GET':
        cmd = f'pgrep stress-ng'
        output = subprocess.run(cmd.split(), capture_output=True)
        print(output)
        if output.returncode != 0:
            response = jsonify({'output': 'No stress test or stressor is running on system'})
        else:
            response = jsonify({'output': 'some stress tests are still running on system'})

        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    else:
        # Handle GET request
        return render_template(request,'stress_cpu.html')



if __name__ == '__main__':
    app.run()
