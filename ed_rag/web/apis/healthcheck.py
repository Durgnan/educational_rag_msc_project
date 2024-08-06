from flask import jsonify

def healthcheck_api(app, session):
    @app.route('/healthcheck', methods=['GET'])
    def healthcheck():
        return jsonify({'status': 'ok'})