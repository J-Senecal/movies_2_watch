from flask_app.static.utils.helpers import api_call


testing = api_call("tarzan")
print(testing['genre'])