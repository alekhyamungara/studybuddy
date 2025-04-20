from flask import Flask
from pywebio.platform.flask import webio_view

from views import sign_up, sign_in, take_test, welcome, habits, home_page

application = Flask(__name__)

# Route registration
#application.add_url_rule('/', 'home', webio_view(home_page), methods=['GET', 'POST'])
application.add_url_rule('/', 'home_page', webio_view(home_page), methods=['GET', 'POST'])
application.add_url_rule('/signup', 'sign_up', webio_view(sign_up), methods=['GET', 'POST'])
application.add_url_rule('/signin', 'sign_in', webio_view(sign_in), methods=['GET', 'POST'])
application.add_url_rule('/test', 'test', webio_view(take_test), methods=['GET', 'POST'])
application.add_url_rule('/welcome', 'welcome', webio_view(welcome), methods=['GET', 'POST'])
application.add_url_rule('/habits', 'habits', webio_view(habits), methods=['GET', 'POST'])

if __name__ == '__main__':
    application.run(debug=True, port=5000)  
