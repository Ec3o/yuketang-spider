import http.client
import json
from config import load_config

config = load_config()

def GetExerciseData():
    conn = http.client.HTTPSConnection('www.yuketang.cn')
    payload = ''
    headers = {
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept': 'application/json, text/plain, */*',
        'Uv-Id': str(config['uv_id']),
        'Classroom-Id': str(config['classroom_id']),
        'Xtbz': config['xtbz'],
        'Cookie': f"sessionid={config['sessionid']}",
        'Host': 'www.yuketang.cn',
        'Connection': 'keep-alive'
    }
    conn.request("GET", f"/mooc-api/v1/lms/exercise/get_exercise_list/{config['exercise_id']}/", payload, headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    return json.loads(data)
