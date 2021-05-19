
from flask_bootstrap import Bootstrap

from apitest.app1.app import app

app.config['SECRET_KEY'] = 'Life is short,You need Taffy!'
bootstrap = Bootstrap(app)
if __name__ == '__main__':
    app.run()
