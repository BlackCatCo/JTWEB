import jtweb

app = jtweb.app()

@app.page('/')
def test():
    return 'Thbop returns'

if __name__ == '__main__':
    app.run()