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
                to: 'akz.982.2004@gmail.com',
                from: 'asfarali7172@gmail.com',
                replyTo: 'asfarali7172@gmail.com',
                subject: '✅ Test Email from Jenkins Pipeline',
                body: 'If you received this email, Jenkins email is working.'
            )
        }
    }
}
