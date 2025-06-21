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
                    sh "docker build -t ${APP_IMAGE} ."
                }
            }
        }

        stage('Build Test Docker Image') {
            steps {
                dir('tests') {
                    sh "docker build -t ${TEST_IMAGE} ."
                }
            }
        }

        stage('Start Application Container') {
            steps {
                sh """
                    docker rm -f taskmanager-app || true
                    docker run -d --name taskmanager-app -p ${APP_PORT}:8081 ${APP_IMAGE}
                    sleep 10
                """
            }
        }

        stage('Run Tests Against App') {
            steps {
                script {
                    // Run tests and capture full output
                    sh "docker run --rm --network host ${TEST_IMAGE} > test-results.txt"

                    // Read full output
                    def fullResults = readFile('test-results.txt')
                    env.FULL_RESULTS = fullResults

                    // Extract summary like:
                    // Passed: 10
                    // Failed: 0
                    def matcher = fullResults =~ /(?m)^\s*Passed:\s*\d+.*\n\s*Failed:\s*\d+/
                    env.TEST_SUMMARY = matcher ? matcher[0] : "Summary not found"
                }
            }
        }
    }

    post {
        success {
            emailext(
                to: 'qasimalik@gmail.com, asfarali7172@gmail.com',
                subject: "✅ Jenkins Build Success: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
Hello,

The Jenkins build completed **successfully**. 🎉

🔹 Job Name: ${env.JOB_NAME}  
🔹 Build Number: ${env.BUILD_NUMBER}  
🔹 Build URL: ${env.BUILD_URL}

📋 **Test Summary**:
${env.TEST_SUMMARY}

Regards,  
Jenkins CI
                """
            )
        }

        failure {
            emailext(
                to: 'qasimalik@gmail.com, asfarali7172@gmail.com',
                subject: "❌ Jenkins Build Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
Unfortunately, the Jenkins build **failed**. ❌

🔹 Job Name: ${env.JOB_NAME}  
🔹 Build Number: ${env.BUILD_NUMBER}  
🔹 Build URL: ${env.BUILD_URL}

📋 **Test Summary**:
${env.TEST_SUMMARY ?: 'No summary available'}

Please check the console output for full logs.

Regards,  
Jenkins CI
                """
            )
        }
    }
}
