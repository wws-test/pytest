

from flask_bootstrap import Bootstrap

from apitest.app import app

app.config['SECRET_KEY'] = 'Life is short,You need Taffy!'
bootstrap = Bootstrap(app)
app.run(debug=True)
