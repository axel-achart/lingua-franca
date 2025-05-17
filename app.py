from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    try:
        data = request.json
        text = data.get('text')
        sl = data.get('sl', 'auto')  # source language
        tl = data.get('tl', 'en')    # target language

        if not text:
            return jsonify({'error': 'No text provided'}), 400

        url = 'https://clients5.google.com/translate_a/t'
        params = {
            'client': 'dict-chrome-ex',
            'sl': sl,
            'tl': tl,
            'q': text
        }

        res = requests.get(url, params=params)
        res.raise_for_status()
        response_data = res.json()

        print(f"Response JSON: {response_data}")

        translation = "No translation found"
        detected_lang = sl
        is_auto_sl = (sl == 'auto')
        temp_translation_parts = []

        try:
            if isinstance(response_data, list) and response_data:
                if (isinstance(response_data[0], list) and response_data[0] and
                    isinstance(response_data[0][0], list) and response_data[0][0] and
                    isinstance(response_data[0][0][0], str)):
                    temp_translation_parts.append(response_data[0][0][0])
                    if is_auto_sl and len(response_data) > 2 and isinstance(response_data[2], str):
                        detected_lang = response_data[2]

                elif (isinstance(response_data[0], list) and response_data[0] and
                      isinstance(response_data[0][0], str)):
                    for item in response_data[0]:
                        if isinstance(item, list) and item and isinstance(item[0], str):
                            temp_translation_parts.append(item[0])
                        elif isinstance(item, str) and not temp_translation_parts:
                            temp_translation_parts.append(item)
                            break
                    if is_auto_sl:
                        if len(response_data) > 2 and isinstance(response_data[2], str):
                            detected_lang = response_data[2]
                        elif len(response_data) > 1 and isinstance(response_data[1], str):
                            detected_lang = response_data[1]

                elif not is_auto_sl and isinstance(response_data[0], str):
                    temp_translation_parts.append(response_data[0])

                elif (is_auto_sl and len(response_data) > 1 and
                      isinstance(response_data[0], str) and isinstance(response_data[1], str)):
                    detected_lang = response_data[1]
                    print(f"Auto-detect: original text '{response_data[0]}', detected language '{detected_lang}'")

            if temp_translation_parts:
                translation = "".join(temp_translation_parts)

        except (IndexError, TypeError, ValueError) as e_parse:
            print(f"Parsing error: {e_parse}. Response data: {response_data}")

        return jsonify({
            'translation': translation,
            'detected_language': detected_lang
        })

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return jsonify({'error': 'Request failed, please try again later.'}), 500
    except Exception as e:
        print(f"General error: {e}")
        return jsonify({'error': 'An unexpected error occurred.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
