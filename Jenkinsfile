pipeline {
    agent any

    environment {
        APP_REPO = 'https://github.com/Asfar-javed/DevOps_TaskManager_3.git'
        TEST_REPO = 'https://github.com/Asfar-javed/DevOps_TaskManager_testcases.git'
        APP_IMAGE = 'taskmanager-app'
        TEST_IMAGE = 'taskmanager-tests'
        APP_PORT = '8081'
    }

    stages {
        stage('Checkout Application') {
            steps {
                dir('app') {
                    git branch: 'main', url: "${APP_REPO}"
                }
            }
        }

        stage('Checkout Tests') {
            steps {
                dir('tests') {
                    git branch: 'main', url: "${TEST_REPO}"
                }
            }
        }

        stage('Build Application Docker Image') {
            steps {
                dir('app') {
                    script {
                        sh 'docker build -t ${APP_IMAGE} .'
                    }
                }
            }
        }

        stage('Build Test Docker Image') {
            steps {
                dir('tests') {
                    script {
                        sh 'docker build -t ${TEST_IMAGE} .'
                    }
                }
            }
        }

        stage('Start Application Container') {
            steps {
                script {
                    sh """
                        docker rm -f taskmanager-app || true
                        docker run -d --name taskmanager-app -p ${APP_PORT}:8081 ${APP_IMAGE}
                        echo "⏳ Waiting for app to start..."
                        sleep 10
                    """
                }
            }
        }

        stage('Run Tests Against App') {
            steps {
                script {
                    sh "docker run --rm --network host ${TEST_IMAGE}"
                }
            }
        }
    }

    post {
        success {
            emailext(
                to: 'qasimalik@gmail.com',
                subject: "✅ Jenkins Build Success: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
Good news! The Jenkins build for your project was successful 🎉

• Job Name: ${env.JOB_NAME}
• Build Number: ${env.BUILD_NUMBER}
• Build URL: ${env.BUILD_URL}

Check it out and continue the great work!
                """
            )
        }
        failure {
            emailext(
                to: 'qasimalik@gmail.com',
                subject: "❌ Jenkins Build Failure: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
Unfortunately, the Jenkins build failed 😞

• Job Name: ${env.JOB_NAME}
• Build Number: ${env.BUILD_NUMBER}
• Build URL: ${env.BUILD_URL}

Please check the console output and logs for further details.
                """
            )
        }
    }
}
