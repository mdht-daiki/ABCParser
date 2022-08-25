import json
from environment.Tune import Tune
from environment.Voice import Voice

class MyEncoder(json.JSONEncoder):
  def default(self, o):
    if isinstance(o, Tune):
      return {'_type': 'Tune', 'value': o.__dict__}
    if isinstance(o, Voice):
      return {'_type': 'Voice', 'value': o.__dict__}           # (*)
    return json.JSONEncoder.default(self, o)

def json_dump(obj):
  return json.dumps(obj, cls=MyEncoder, indent=4)