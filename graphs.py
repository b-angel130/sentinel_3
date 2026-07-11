#graphs.py
class BandwidthGraph:

    def __init__(self):

        self.upload = []

        self.download = []

    def add(self, up, down):

        self.upload.append(up)

        self.download.append(down)

        if len(self.upload) > 60:
            self.upload.pop(0)

        if len(self.download) > 60:
            self.download.pop(0)