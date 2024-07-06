import jtclient as jtc
import mdrender as mdr

TITLE = 'JWEB Client'


class App():
    def __init__(self):
        self.client = jtc.app()
        self.client.setup_dns('127.0.0.1', 4242)

        self.renderer = mdr.app(1200, 800, TITLE)
        self.renderer.link_click_action = self.search
        self.search_bar = self.renderer.txtboxes.add((4, 10), 1000, 'thbop.code/')
        self.search_bar.action_enter = self.search_enter
    
    def search_enter(self, txtbox: mdr.TextBox):
        self.search(txtbox.value)
    
    def search(self, raw_search: str):
        slash_pos = raw_search.find('/')

        domain = raw_search[0:slash_pos]
        route = raw_search[slash_pos:len(raw_search)]
        self.client.connect(domain)
        self.client.request(route)

        self.renderer.title = TITLE + ' -> ' + domain

        self.renderer.compile_md(self.client.get_incoming_text())
        
    
    def run(self):
        self.renderer.run()


if __name__ == '__main__':
    app = App()
    app.run()