from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
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

    try:
        res = requests.get(url, params=params)
        res.raise_for_status()
        response_data = res.json()

        # More detailed logging for debugging
        print(f"Response JSON for input: {{'text': text, 'sl': sl, 'tl': tl}}, is: {response_data}")

        translation = "No translation found"
        # Default detected_lang to sl; if sl='auto', it might be updated by parsing.
        # If not updated by parsing and sl was 'auto', it remains 'auto', which client can handle.
        detected_lang = sl 
        is_auto_sl = (sl == 'auto')

        try:
            if not isinstance(response_data, list) or not response_data:
                print(f"Unexpected response_data format (not a list or empty): {response_data}")
            else:
                temp_translation_parts = []

                # Attempt 1: Check for the most explicit nested structure first.
                # e.g., [[["translated_text_to_tl", "original", ...]], null, "detected_sl", ...]
                if (isinstance(response_data[0], list) and len(response_data[0]) > 0 and
                    isinstance(response_data[0][0], list) and len(response_data[0][0]) > 0 and
                    isinstance(response_data[0][0][0], str)):
                    temp_translation_parts.append(response_data[0][0][0])
                    if is_auto_sl and len(response_data) > 2 and isinstance(response_data[2], str) and response_data[2]:
                        detected_lang = response_data[2]
                
                # Attempt 2: Check for simpler list structure where response_data[0] is a list of segments/translations.
                # e.g., [["translated_segment1_to_tl", ...], ["translated_segment2_to_tl", ...]]
                # or just [["translated_text_to_tl", "original_text", ...]]
                elif (isinstance(response_data[0], list) and len(response_data[0]) > 0 and
                      isinstance(response_data[0][0], str)): # First item of first sublist is a string
                    for segment_list_item in response_data[0]:
                        # If response_data[0] is like [["trans1", "orig1"], ["trans2", "orig2"]], iterate through these pairs.
                        if isinstance(segment_list_item, list) and segment_list_item and isinstance(segment_list_item[0], str):
                            temp_translation_parts.append(segment_list_item[0])
                        # If response_data[0] is just like ["trans1", "orig1", ...], only the first iteration will run.
                        elif isinstance(segment_list_item, str) and not temp_translation_parts: # take the first string if it's a flat list
                            temp_translation_parts.append(segment_list_item)
                            break # Only take the first item as translation if structure is like ["trans", "orig", ...]
                            
                    if is_auto_sl:
                        if len(response_data) > 2 and isinstance(response_data[2], str) and response_data[2]:
                            detected_lang = response_data[2]
                        elif len(response_data) > 1 and isinstance(response_data[1], str) and len(response_data[1]) == 2:
                             detected_lang = response_data[1]
                
                # Attempt 3: Simplest structure ["translated_text_to_tl"] (ONLY if sl is EXPLICIT)
                elif (not is_auto_sl and isinstance(response_data[0], str)):
                    temp_translation_parts.append(response_data[0])
                    # detected_lang remains sl (explicitly set)
                
                # Attempt 4: Handle sl='auto' when API returns [original_text, detected_lang_code]
                elif (is_auto_sl and len(response_data) > 1 and
                      isinstance(response_data[0], str) and isinstance(response_data[1], str) and len(response_data[1]) == 2):
                    detected_lang = response_data[1] # Set detected language
                    # translation remains "No translation found" as response_data[0] is original text
                    print(f"Auto-detect mode: API returned original text '{response_data[0]}' and detected language '{detected_lang}'. "
                          f"This response format does not include translation to the target language '{tl}'.")

                if temp_translation_parts:
                    translation = "".join(temp_translation_parts)
                # If is_auto_sl and translation is still "No translation found", it implies the API didn't provide
                # a direct translation to 'tl' in a recognized format for auto-detection.

        except (IndexError, TypeError, ValueError) as e_parse:
            print(f"Error during parsing of translation response: {e_parse}. Response data: {response_data}")
            # translation will remain "No translation found", detected_lang will use its default

        return jsonify({
            'translation': translation,
            'detected_language': detected_lang
        })
    
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return jsonify({'error': 'Request failed, please try again later.'}), 500
    except Exception as e:
        print(f"General error: {e}") # Catch any other errors, including JSONDecodeError if res.json() fails
        return jsonify({'error': 'An unexpected error occurred processing your request.'}), 500

if __name__ == '__main__':
    app.run(debug=True)