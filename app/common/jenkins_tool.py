import jenkins

jenkins_server_url = "https://jenkins.zhito.com"
user_id = "wangshiyuan"
api_token = "11bdffee022bd22472efdf2ebd99354522"
server=jenkins.Jenkins(jenkins_server_url, username=user_id, password=api_token)
job = "integration_test3" # 每个项目对应一个job?

def build(job, parameters):
    try:
        # 查询下一次build的number
        nextBuildNumber = server.get_job_info(job)['nextBuildNumber']
        print("\nextBuildNumber: ", nextBuildNumber)

        # 构建job
        build_queue = server.build_job(job, parameters)
        return {
            "build_number": nextBuildNumber,
            "build_queue": build_queue
        }
    except Exception as e:
      print('An exception occurred in jenkins build', str(e))

