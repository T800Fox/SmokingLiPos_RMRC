import flask
from flask import request, jsonify
from adafruit_servokit import ServoKit

app = flask.Flask(__name__)
app.config["DEBUG"] = True

servos = [
    {
        'id' : 'MG995-1',
        'range' : 120,
        'position_rest' : 0,
        'position_current' : 0,
        'address' : 0
    },
    {
        'id' : 'MG995-2',
        'range' : 120,
        'position_rest' : 0,
        'position_current' : 0,
        'address' : 1
    },
    {        
        'id' : '225MG-1',
        'range' : 180,
        'position_rest' : 0,
        'position_current' : 0,
        'address' : 2
    },
    {        
        'id' : '225MG-2',
        'range' : 180,
        'position_rest' : 0,
        'position_current' : 0,
        'address' : 3
    },
    {        
        'id' : 'SG90-1',
        'range' : 180,
        'position_rest' : 0,
        'position_current' : 0,
        'address' : 4
    },
    {        
        'id' : 'SG90-2',
        'range' : 180,
        'position_rest' : 0,
        'position_current' : 0,
        'address' : 5
    }
]

#   setup servos:
print("Initalizing Servos...")
kit = ServoKit(channels=16)
for i in servos:
    kit.servo[i['address']].actuation_range = i['range']
    kit.servo[i['address']].angle = i['position_rest']
print("Complete")

@app.route('/api/servo_v1/all', methods=['GET'])
def api_all():
    return jsonify(servos)

@app.route('/api/servo_v1/getPosition', methods=['GET'])
def api_getPosition():
    if 'id' in request.args:
        id = str(request.args['id']).upper()
        for i in servos:
            if id == i['id']:
                return jsonify({'position' : i['position_current']})        
        return "ERROR: invalid id"
    else:
        return "ERROR: no id specified"

@app.route('/api/servo_v1/setPosition', methods=['GET'])
def api_setPosition():
    #   check the servo exists:
    if 'id' in request.args:
        id = str(request.args.get('id')).upper()
        flag = False
        for i in servos:
            if id == i['id']:
                flag = True
        if flag == False:
            return "ERROR: invalid id"
    else:
        return "ERROR: no id specified"

    #   check the position is valid and update if it is:
    if 'position' in request.args:
        try:
            position = int(request.args.get('position'))
        except:
            return "ERROR: position is not int"
        if position < 0:
            return "ERROR: position must be positive value"
        
        
        for i in servos:
            if id == i['id'] and position <= i['range']:
                print("Setting " + i['id'] + " to " + str(position))
                i['position_current'] = position
                kit.servo[i['address']].angle = i['position_current']
                print(i['position_current'])
                return 'success', 200
            elif id == i['id'] and position > i['range']:
                return "ERROR: specified position is out of range for servo, " + str(position) + " was supplied when the range for the servo is " + str(i['range'])
    else:
        return "ERROR: no position specified"

@app.route('/api/servo_v1/restPositions', methods=['GET'])
def api_restPositions():
    for i in servos:
        kit.servo[i['address']].angle = i['position_rest']
    return 'success', 200

app.run()