import jenkins
from Model import Api_process, App_process
from exts import db
session = db.session

jenkins_server_url = "https://jenkins.zhito.com"
user_id = "wangshiyuan"
api_token = "11bdffee022bd22472efdf2ebd99354522"
server=jenkins.Jenkins(jenkins_server_url, username=user_id, password=api_token)

# 构建job
def build(job, parameters):
    try:
        # 查询下一次build的number
        nextBuildNumber = server.get_job_info(job)['nextBuildNumber']

        # 构建job
        build_queue = server.build_job(job, {"param": parameters})
        return {
            "build_number": nextBuildNumber,
            "build_queue": build_queue
        }
    except Exception as e:
      print('An exception occurred in jenkins build', str(e), flush=True)

# 更新任务状态
def update_build_state(data, type="Api_process"):
    try:
        for item in data:
            info = get_build_info(item[1], item[2], item[3])
            # 单更新url
            if (info["state"] == 2 and info["url"] is not None):

                if type == "Api_process":
                    session.query(Api_process).filter(Api_process.id == item[0]).update({
                        "jenkins_url": info["url"]
                    })
                    session.commit()
                    session.close()
                if type == "App_process":
                    session.query(App_process).filter(App_process.id == item[0]).update({
                        "jenkins_url": info["url"]
                    })
                    session.commit()
                    session.close()
            # 更新url和状态
            if (info["state"] > 2):
                if type == "Api_process":
                    session.query(Api_process).filter(Api_process.id == item[0]).update({
                        "state": info["state"],
                        "jenkins_url": info["url"]
                    })
                    session.commit()
                    session.close()
                if type == "App_process":
                    session.query(App_process).filter(App_process.id == item[0]).update({
                        "state": info["state"],
                        "jenkins_url": info["url"]
                    })
                    session.commit()
                    session.close()
    except Exception as e:
        session.rollback()
        print('An exception occurred at update_build_state', str(e), flush=True)


#  办法：
#  1.build前假定该次build_number = nextBuildNumber, 记录queueId
#  2.查询build_info前, 先查询lastbuildNumber, 
#    2.1 lastBuildNumber < build_number, 直接返回, 认为build进行中, 需要等一会再查询
#    2.2 lastBuildNumber >= build_number时, 查询buildInfo
#    2.3 比较buildInfo.queueId和记录的queueId
#    2.4 如果相等,返回buildInfo
#    2.5 如果不相等, build_number = build_number + 1, 重复执行步骤2
#  tips:build之后不能立即查询到build_number,等待时间不确定

# 查询job状态
def get_build_info(job, build_number, build_queue):
    try:
        # 查询job最后一次build的number, 判断当前能否查询到
        last_build_number = server.get_job_info(job)['lastBuild']['number']
        if last_build_number < build_number:
            # 目前还查询不到
            return {
                "state": 2,
                 "url": None
            }
        else:
            # 查询build_info, 比对queue
            build_info = server.get_build_info(job, build_number)
            # 相等时, 认为是这个build
            if build_queue == build_info["queueId"]:
                # 未构建结束，更新url
                if build_info["result"] is None:
                    return {
                        "state": 2,
                        "url": build_info["url"]
                    }
                else:
                    # 构建结束，更新结果、状态
                    return {
                        "state": 3 if build_info["result"].lower() == "success" else 4,
                        "url": build_info["url"]
                    }
            # 否则认为是下一次构建
            else:
                return get_build_info(job, build_number + 1, build_queue)

    except Exception as e:
      print('An exception occurred in jenkins get_build_info', str(e), flush=True)


def schedule_task():
    try:
        # 待更新状态的数据
        runningData = session.query(App_process.id, App_process.job_name, App_process.build_number, App_process.build_queue).filter(App_process.state == 2).all()
        session.close()
        update_build_state(runningData, "App_process")
    except Exception as e:
        print('An exception occurred in schedule_task', str(e), flush=True)
