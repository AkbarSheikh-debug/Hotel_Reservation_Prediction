pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = "modular-glider-462609-u1"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
        PIP_NO_CACHE_DIR = 'off'
    }

    stages {
        stage('Cloning Github repo to Jenkins') {
            steps {
                script {
                    echo 'Cloning Github repo to Jenkins............'
                    checkout scmGit(
                        branches: [[name: '*/main']],
                        extensions: [],
                        userRemoteConfigs: [[
                            credentialsId: 'Github-Token',
                            url: 'https://github.com/AkbarSheikh-debug/Hotel_Reservation_Prediction.git'
                        ]]
                    )
                }
            }
        }

        stage('Setting up Virtual Environment and Installing Dependencies') {
            steps {
                script {
                    echo 'Setting up Virtual Environment and Installing Dependencies............'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    '''
                }
            }
        }
    
    }
}
