import json
import base64

def encode_json_to_base64(json_obj):
    json_str = json.dumps(json_obj)
    json_bytes = json_str.encode('utf-8')
    base64_bytes = base64.b64encode(json_bytes)
    base64_str = base64_bytes.decode('utf-8')
    return base64_str

def decode_base64_to_json(base64_str):
    json_bytes = base64.b64decode(base64_str)
    json_str = json_bytes.decode('utf-8')
    json_obj = json.loads(json_str)
    return json_obj