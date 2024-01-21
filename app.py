from flask import Flask, jsonify, request
import logging

app = Flask(__name__)

# Configure logging to capture detailed information
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def hello_world():
    try:
        app.logger.debug('Accessing the Hello World endpoint')
        return 'Hello, World!'
    except Exception as e:
        app.logger.error('Error in Hello World endpoint: %s', e)
        return jsonify(error=str(e)), 500

@app.route('/health')
def health_check():
    try:
        app.logger.debug('Performing health check')
        return jsonify({"status": "healthy"}), 200
    except Exception as e:
        app.logger.error('Error in health check: %s', e)
        return jsonify(error=str(e)), 500

@app.errorhandler(404)
def page_not_found(e):
    app.logger.error('Page not found: %s', e)
    return jsonify(error=str(e)), 404

@app.errorhandler(500)
def internal_server_error(e):
    app.logger.error('Internal server error: %s', e)
    return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0')
