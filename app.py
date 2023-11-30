from flask import Flask, jsonify, request, stream_with_context, Response
from flask_restful import Api
import json
from controller.i2c import I2CBridge
from controller.camera import VideoCamera, gen
import sys

app = Flask(__name__)
api = Api(app)
port = 8080

if len(sys.argv) > 1:
    port = int(sys.argv[1])
print("Api running on port : {} ".format(port))

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
        print(e)
        response = jsonify({"error": str(e), "number": payload.get("number")})
        response.status_code = 500

    return response


@app.route("/camera", methods=["GET"])
def camera_view():
    # get the ID from the path
    id = int(request.args.get('id'))
    if (id == None):
        id = 0

    @stream_with_context
    def generate():
        try:

            # create the video camera object
            # the camera will be opened when the thread starts (camera.start())
            camera = VideoCamera(id)
            camera.start()

            for frame in gen(camera):
                yield frame

        except Exception as e:
            print("error::", e)
            yield "Error" + str(e)
        finally:
            camera.stop()
    
    return Response(generate(), content_type="multipart/x-mixed-replace;boundary=frame")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port)