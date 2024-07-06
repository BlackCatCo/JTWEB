import jtweb

app = jtweb.app()

app.setup_dns()

@app.page('/')
def test():
    return '''Hello World!

[Cool Page](/bobbyj) <---- Check this out!!

[Error 4 page](/asdfasdf) <---- Don't click
'''

@app.page('/bobbyj')
def test2():
    return '''Bobby J returns

[back](/)
'''

if __name__ == '__main__':
    app.run()