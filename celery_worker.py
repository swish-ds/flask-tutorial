from flaskr import celery, create_app
import app_config

app = create_app(app_config.Config)
app.app_context().push()
