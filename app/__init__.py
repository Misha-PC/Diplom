from config import ApplicationConfiguration
from flask import Flask

webApp = Flask(__name__)
webApp.config.from_object(ApplicationConfiguration)

import app.view
