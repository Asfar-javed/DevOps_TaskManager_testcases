pipeline {
    agent any

    stages {
        stage('Test') {
            steps {
                echo 'Just testing email'
            }
        }
    }

    post {
        success {
            emailext(
    to: 'asfarali7172@gmail.com',
    from: 'asfarali7172@gmail.com',
    subject: '✅ Test Email from Jenkins Pipeline',
    mimeType: 'text/plain',
    body: 'If you received this email, Jenkins email is working.'
)

        }
    }
}
