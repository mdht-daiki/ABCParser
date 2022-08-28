class Voice:
    def __init__(self):
        self.name = ""
        self.body = []
        self.param = {}

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def append_body(self, note):
        self.body.append(note)

    def set_param(self, key, value):
        self.param[key] = value
    
    def get_params(self):
        return self.param
    
    def get_body(self):
        return self.body

    def get_last_note(self):
        return self.body[-1]
