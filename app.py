from flask import Flask, render_template, request, jsonify
import sys
import os
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

try:
    from substitution_cipher import SubstitutionCipher

    logger.debug("Successfully imported SubstitutionCipher")
except ImportError as e:
    logger.error(f"Error importing substitution_cipher: {e}")
    sys.exit(1)

import random
from time import time

app = Flask(__name__)

# Initialize cipher
random.seed(int(time()))
try:
    cipher = SubstitutionCipher()
    logger.debug("Cipher initialized with key: %s", cipher.key)
except Exception as e:
    logger.error("Failed to initialize cipher: %s", str(e))
    sys.exit(1)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process_text():
    try:
        data = request.get_json()
        if not data or 'text' not in data or 'action' not in data:
            logger.error("Invalid request data: %s", data)
            return jsonify({'error': 'Invalid request: text and action are required'}), 400

        text = data['text'].strip()
        action = data['action'].strip().lower()

        logger.debug("Received request - Text: %s, Action: %s", text, action)

        if not text or not action:
            logger.error("Empty text or action")
            return jsonify({'error': 'Text and action cannot be empty'}), 400

        if action == 'encrypt':
            result = cipher.encrypt(text)
        elif action == 'full_decrypt':
            result = cipher.full_decrypt(text)
        elif action == 'simple_decrypt':
            result = cipher.decrypt(text)
        elif action == 'reverse_sub':
            result = cipher.substitute_names_in_text(text, False)
        else:
            logger.error("Invalid action: %s", action)
            return jsonify({'error': f'Invalid action: {action}'}), 400

        logger.debug("Processed result: %s", result)
        return jsonify({'result': result})

    except Exception as e:
        logger.error("Error processing request: %s", str(e), exc_info=True)
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)