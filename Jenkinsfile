pipeline {
    agent any 

    environment {
        VENV_DIR = 'venv'
    }

    stages {
        stage('Cloning GitHub Repo to Jenkins') {
            steps {
                script {
                    echo 'Cloning GitHub repo to Jenkins............'
                    checkout scmGit(
                        branches: [[name: '*/main']], 
                        extensions: [], 
                        userRemoteConfigs: [[
                            credentialsId: 'Github-Token', 
                            url: 'https://github.com/AkbarSheikh-debug/Hotel_Reservation_Prediction.git'
                        ]
                    )
                }
            }
        }

        stage('Setting up Virtual Environment and Installing Dependencies') {
            steps {
                script {
                    echo 'Setting up Virtual Environment and Installing Dependencies............'
                    sh '''
                    set -e  # Fail on first error

                    # Use python3 explicitly
                    python3 -m venv ${VENV_DIR}

                    # Use pip directly from venv (no need to source activate)
                    ${VENV_DIR}/bin/pip install --upgrade pip
                    ${VENV_DIR}/bin/pip install -e .
                    '''
                }
            }
        }
    }
}
