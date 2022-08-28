from .Environment import Environment


class Tune(Environment):
    def __init__(self, parent_env):
        super().__init__(parent_env)
        self.voice = {}

    def set_voice(self, voice):
        self.voice[voice.get_name()] = voice

    def get_voice(self, name):
        return self.voice[name]
    
    def get_voices(self):
        return self.voice

    def push_note(self, voice, note):
        self.voice[voice].append_body(note)
