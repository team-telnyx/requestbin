pipeline {
    agent any

    environment {
        SERVICE_NAME = 'requestbin'
        TARGET_HOSTS = 'dev_messaging_ch1_01'  // need to keep on same redis cluster
        SLACK_CHANNEL = 'squad-messaging-jenk'
    }

    stages {
        stage('Build') {
            steps {
                echo 'Building...'
                slackSend (
                    channel: "${SLACK_CHANNEL}",
                    color: "#738595",
                    message: "Starting Job: ${env.JOB_NAME} #${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)",
                )
                sh 'make build'
            }
            post {
                failure {
                    slackSend(
                        channel: "${SLACK_CHANNEL}",
                        color: "#fe0002",
                        message: "Failed Build: ${env.JOB_NAME} #${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)",
                    )
                }
            }
        }
        stage('Push to registry') {
            steps {
                echo 'Pushing to registry'
                sh 'make push'
            }
            post {
                failure {
                    slackSend(
                        channel: "${SLACK_CHANNEL}",
                        color: "#fe0002",
                        message: "Failed Pushing: ${env.JOB_NAME} #${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)",
                    )
                }
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying...'
                ansiblePlaybook(
                    installation: 'ansible2140',
                    inventory: '/etc/ansible/hosts-all',
                    playbook: '/etc/ansible/playbooks/autodeploy/pushnewcontainers_red_AT.yml',
                    credentialsId: 'telnyx-jenkinsipa-credentials',
                    extras: '-e "service=${SERVICE_NAME} targethosts=${TARGET_HOSTS}"'
                )
            }
            post {
                failure {
                    slackSend(
                        channel: "${SLACK_CHANNEL}",
                        color: "#fe0002",
                        message: "Failed Deployment: ${env.JOB_NAME} #${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)",
                    )
                }
            }
        }
    }
    post {
        success {
            slackSend (
                channel: "${SLACK_CHANNEL}",
                color: "#02c14d",
                message: "Success! ${env.JOB_NAME} #${env.BUILD_NUMBER}",
            )
        }
    }
}
