import jtweb

app = jtweb.app()

app.setup_dns()

@app.page('/')
def test():
    return 'Thbop returns'

@app.page('/bobbyj')
def test2():
    return 'Bobby J returns'

if __name__ == '__main__':
    app.run()