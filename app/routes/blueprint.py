
def registerRoute(app):
    BASE_URL_PREFIX = "/api"

    # 公告
    from .api_process import api_process
    app.register_blueprint(api_process, url_prefix=BASE_URL_PREFIX + "/api_process")
