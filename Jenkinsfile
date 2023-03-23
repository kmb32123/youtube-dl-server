pipeline {
    agent any

    options {
        disableConcurrentBuilds()
    }

    stages {
        stage('Checkout'){
            steps {
                checkout scm
            }
        }
        stage('Prep buildx') {
            steps {
                script {
                    env.BUILDX_BUILDER = getBuildxBuilder();
                }
            }
        }
        stage('Dockerhub login') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKERHUB_CREDENTIALS_USR', passwordVariable: 'DOCKERHUB_CREDENTIALS_PSW')]) {
                    sh 'docker login -u $DOCKERHUB_CREDENTIALS_USR -p "$DOCKERHUB_CREDENTIALS_PSW"'
                }
            }
        }
        stage('Build Youtube-dl Image') {
            steps {
                sh """
                    docker buildx build --pull --builder \$BUILDX_BUILDER  --platform linux/amd64,linux/arm64,linux/arm/v7 --build-arg ATOMICPARSLEY=1 -t nbr23/youtube-dl-server:latest -t nbr23/youtube-dl-server:youtube-dl -t nbr23/youtube-dl-server:youtube-dl_atomicparsley --push .
                    """
            }
        }

        stage('Build Youtube-dl yt_dlp Image') {
            steps {
                sh """
                    docker buildx build --pull --builder \$BUILDX_BUILDER  --platform linux/amd64,linux/arm64,linux/arm/v7 --build-arg YOUTUBE_DL=yt_dlp --build-arg ATOMICPARSLEY=1 -t nbr23/youtube-dl-server:yt-dlp -t nbr23/youtube-dl-server:yt-dlp_atomicparsley -f Dockerfile-ytdlp --push .
                    """
            }
        }
        stage('Sync github repo') {
            when { branch 'master' }
            steps {
                syncRemoteBranch('git@github.com:nbr23/youtube-dl-server.git', 'master')
            }
        }
    }
    post {
        always {
            sh 'docker buildx stop $BUILDX_BUILDER || true'
            sh 'docker buildx rm $BUILDX_BUILDER'
        }
    }
}