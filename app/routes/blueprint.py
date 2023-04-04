
def registerRoute(app):
    BASE_URL_PREFIX = "/api"

    # 接口集成
    from .api_process import api_process
    app.register_blueprint(api_process, url_prefix=BASE_URL_PREFIX + "/api_process")

    # 项目
    from .project import project
    app.register_blueprint(project, url_prefix=BASE_URL_PREFIX + "/project")

    # gitlab、jenkins、artifactory
    from .tools import tools
    app.register_blueprint(tools, url_prefix=BASE_URL_PREFIX)
