import jtweb
import os
os.chdir(os.path.dirname(__file__))

app = jtweb.app()

app.setup_dns()

@app.page('/')
def test():
    return '''Hello World!

[Cool Page](thbop.code/bobbyj) <---- Check this out!!

[Error 4 page](thbop.code/asdfasdf) <---- Don't click
'''

@app.page('/bobbyj')
def test2():
    return '''Bobby J returns

[back](thbop.code/)
'''

if __name__ == '__main__':
    app.run()