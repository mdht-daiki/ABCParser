import json
from environment.Tune import Tune
from environment.Note import Note
from environment.Voice import Voice
from notelength.Length import Length
from pitch.Accidental import Accidental
from pitch.Key import Key


class MyEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (Tune, Note, Voice, Key, Accidental)):
            return {'_type': o.__class__.__name__, 'value': o.__dict__}
        # if isinstance(o, Voice):
        #   return {'_type': 'Voice', 'value': o.__dict__}
        if isinstance(o, Length):
            return {'_type': o.__class__.__name__, 'value': str(o)}
        return json.JSONEncoder.default(self, o)


def json_dump(obj):
    return json.dumps(obj, cls=MyEncoder, indent=4)
