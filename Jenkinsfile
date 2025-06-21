pipeline {
    agent any

    environment {
        EMAIL_CREDENTIALS_ID = 'gmail-creds'  // ID you gave above
    }

    stages {
        stage('Test') {
            steps {
                echo 'Just testing email'
            }
        }
    }

    post {
        success {
            script {
                emailext(
                    to: 'asfarali7172@gmail.com',
                    from: 'asfarali7172@gmail.com',
                    replyTo: 'asfarali7172@gmail.com',
                    subject: '✅ Test Email from Jenkins Pipeline',
                    mimeType: 'text/plain',
                    body: 'If you received this email, Jenkins email is working.',
                    recipientProviders: [[$class: 'DevelopersRecipientProvider']],
                    attachLog: false,
                    compressLog: false,
                    credentialsId: "${env.EMAIL_CREDENTIALS_ID}"
                )
            }
        }
    }
}
