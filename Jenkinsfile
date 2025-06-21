pipeline {
    agent any 

    environment {
        VENV_DIR = 'venv'
        PIP_NO_CACHE_DIR = 'off'
    }

    stages {
        stage('Cloning GitHub Repo') {
            steps {
                script {
                    echo 'Cloning GitHub repo...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'Github-Token', url: 'https://github.com/AkbarSheikh-debug/Hotel_Reservation_Prediction.git']])
                }
            }
        }

        stage('Setting up Virtual Environment and Installing Dependencies') {
            steps {
                script {
                    echo 'Setting up Virtual Environment...'
                    sh '''
                    set -e
                    python3 -m venv ${VENV_DIR}
                    ${VENV_DIR}/bin/pip install --upgrade pip --trusted-host pypi.org --trusted-host files.pythonhosted.org
                    ${VENV_DIR}/bin/pip install -e . --trusted-host pypi.org --trusted-host files.pythonhosted.org
                    '''
                }
            }
        }
    }
}
