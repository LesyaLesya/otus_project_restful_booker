pipeline {
    agent any

    stages {
        stage('DockerBuild') {
            steps {
                echo 'Building docker image with tag tests'
                sh '/usr/local/bin/docker build -t tests .'
            }
        }
        stage('TestRun') {
            steps {
                echo 'Running tests in container'
                sh '''
                   if [ -m "$MARKER" ]
                   then
                   /usr/local/bin/docker run --name my_container tests --login ${LOGIN} --passw ${PASSW} -n ${NODES} -m ${MARKER}
                   else
                   /usr/local/bin/docker run --name my_container tests --login ${LOGIN} --passw ${PASSW} -n ${NODES}
                   fi
                '''
            }
        }
    }

    post {

        always {
            echo 'Copying allure report from container'
            sh '/usr/local/bin/docker cp my_container:/app/allure-results .'

            script {
                allure([
                        includeProperties: false,
                        jdk: '',
                        properties: [],
                        reportBuildPolicy: 'ALWAYS',
                        results: [[path: 'allure-results']]
                ])
            }
            echo 'Deleting container and image'
            sh '/usr/local/bin/docker system prune -f'
            sh '/usr/local/bin/docker image rm tests'


            cleanWs()
        }
    }
}
