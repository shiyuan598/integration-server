import jenkins

jenkins_server_url = "https://jenkins.zhito.com"
user_id = "wangshiyuan"
api_token = "11bdffee022bd22472efdf2ebd99354522"
server=jenkins.Jenkins(jenkins_server_url, username=user_id, password=api_token)

# 构建job
def build(job, parameters):
    try:
        job = "integration_test4"
        print("参数：", parameters)
        # 查询下一次build的number
        nextBuildNumber = server.get_job_info(job)['nextBuildNumber']
        print("\nextBuildNumber: ", nextBuildNumber)

        # 构建job
        build_queue = server.build_job(job, {"param": parameters})
        print("\nbuild_queue: ", build_queue)
        return {
            "build_number": nextBuildNumber,
            "build_queue": build_queue
        }
    except Exception as e:
      print('An exception occurred in jenkins build', str(e))

# 查询job状态
def get_build_info(job, build_number, build_queue):
    try:
        # 查询job最后一次build的number, 判断当前能否查询到
        last_build_number = server.get_job_info(job)['lastBuild']['number']
        print("\nlast_build_number: ", last_build_number)
        if last_build_number < build_number:
            return {
                "state": 2
            }
        else:
            # 查询build_info, 比对queue
            build_info = server.get_build_info(job, build_number)
            # 相等时, 认为是这个build
            if build_queue == build_info["queueId"]:
                return {
                    "state": 3 if build_info["result"].lower() == "success" else 4,
                    "result": build_info["result"],
                    "url": build_info["url"]
                }
            # 否则认为是下一次构建
            else:
                return get_build_info(job, build_number + 1, build_queue)

    except Exception as e:
      print('An exception occurred in jenkins get_build_info', str(e))

#  办法：
#  1.build前假定该次build_number = nextBuildNumber, 记录queueId
#  2.查询build_info前, 先查询lastbuildNumber, 
#    2.1 lastBuildNumber < build_number, 直接返回, 认为build进行中, 需要等一会再查询
#    2.2 lastBuildNumber >= build_number时, 查询buildInfo
#    2.3 比较buildInfo.queueId和记录的queueId
#    2.4 如果相等,返回buildInfo
#    2.5 如果不相等, build_number = build_number + 1, 重复执行步骤2
#  tips:build之后不能立即查询到build_number,等待时间不确定