from flask import Flask, jsonify, request, stream_with_context, Response
import json
from .controller.i2c import I2CBridge
from .controller.camera import VideoCamera, gen

app = Flask(__name__)

@app.route("/controller", methods=["POST"])
def controller():
    try:
        # load the json data
        payload = json.loads(request.get_json())

        robot = I2CBridge()
        if (payload.get("type") == "movement"):
            robot.move_speed(payload.get("type"), payload.get("command"), int(payload.get("speed")))
        else:
            robot.move(payload.get("type"), payload.get("command"))

        response = jsonify({"number": payload.get("number")})
        response.status_code = 200

    except Exception as e:
        response = jsonify({"error": str(e), "number": payload.get("number")})
        response.status_code = 500

    return response


@app.route("/camera", methods=["GET"])
def camera_view():
    @stream_with_context
    def generate():

        try:
            camera = VideoCamera(request.args.get('id'))
            response = Response(gen(camera), content_type="multipart/x-mixed-replace;boundary=frame")
            response['Cache-Control'] = 'no-cache'
            camera.response = response
            camera.start()
        except Exception as e:
            response = Response({"error": e})
            response.status_code = 500
        return response
    return generate()