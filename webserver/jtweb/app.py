

class app:
    def __init__(self):
        self.pages = []

    def page(self, pg):
        self.pages.append(pg)
    
    def run(self):
        for p in self.pages:
            p()