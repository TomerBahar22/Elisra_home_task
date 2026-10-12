def repoUrl    = 'https://github.com/TomerBahar22/Elisra_home_task.git'
def branchName = binding.hasVariable('BRANCH') ? BRANCH : 'main'

def jobs = [
    [name: '01-build-flask',   script: 'jenkins/pipelines/Jenkinsfile.flask',
     desc: 'Build the Flask app image and push it to Docker Hub'],
    [name: '02-build-nginx',   script: 'jenkins/pipelines/Jenkinsfile.nginx',
     desc: 'Build the Nginx reverse-proxy image and push it to Docker Hub'],
    [name: '03-deploy-verify', script: 'jenkins/pipelines/Jenkinsfile.deploy',
     desc: 'Run both containers, expose Nginx on localhost only, verify'],
]

jobs.each { j ->
    pipelineJob(j.name) {
        description(j.desc)
        definition {
            cpsScm {
                scm {
                    git {
                        remote { url(repoUrl) }
                        branch("*/${branchName}")
                    }
                }
                scriptPath(j.script)
                lightweight(true)
            }
        }
    }
}