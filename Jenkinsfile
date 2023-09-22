pipeline {
    agent any

    stages {
        stage('DockerBuild') {
            steps {
                echo 'Building docker image with tag tests'
                sh '${DOCKER_PATH} build -t tests .'
            }
        }
        stage('TestRun') {
            steps {
                echo 'Running tests in container'
                sh '''
                   if [ "$MARKER" == "all_tests" ]
                   then
                   ${DOCKER_PATH} run --name my_container tests -n ${NODES} --schema ${SCHEMA} --host ${HOST} --login ${LOGIN} --passw ${PASSW}
                   else
                   ${DOCKER_PATH} run --name my_container tests -n ${NODES}  -m ${MARKER} --schema ${SCHEMA} --host ${HOST} --login ${LOGIN} --passw ${PASSW}
                   fi
                '''
            }
        }
    }

    post {

        always {
            echo 'Copying allure report from container'
            sh '${DOCKER_PATH} cp my_container:/app/allure-results .'

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
            sh '${DOCKER_PATH} system prune -f'
            sh '${DOCKER_PATH} image rm tests'


            cleanWs()
        }
    }
}
