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

    def push_line(self, voice, line):
        self.voice[voice].append_body(line)

    # bodyの出力順をABC表記の形式通りにするgenerator
    # voice1の1行目 -> voice2の1行目 -> ... -> voiceNの1行目 -> voice1の2行目 -> ...
    def body_generator(self):
      bodies = []
      voices = self.voice.values()
      for voice in voices:
        bodies.append(voice.get_body())
        # bodies = [voice1.body, voice2.body, ... , voiceN.body]
      for lines in zip(*bodies):
        # lines = (voice1のbody1行目, voice2のbody1行目, ... )
        for line, voice in zip(lines, voices):
          yield line, voice.get_name()
    
    def get_finger_list(self):
        finger_list = []
        bg = self.body_generator()
        for line, _ in bg:
            finger_list_line = []
            for note in line:
                finger_list_line.append(note.get_fingering())
            finger_list.append(finger_list_line)
        return finger_list
    
    def set_fingers(self, finger_list):
        bg = self.body_generator()
        finger_list_index = 0
        for line, _ in bg:
            for note, finger in zip(line, finger_list[finger_list_index]):
                note.set_fingerings(finger)
            finger_list_index += 1
            