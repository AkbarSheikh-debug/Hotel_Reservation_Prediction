pipeline{
  agent any 

  stages {
    stage("Cloning Github repo to Jenkins"){
      steps{
        script{
          echo 'Cloning Github repo to Jenkins....................'
          checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'Github-Token', url: 'https://github.com/AkbarSheikh-debug/Hotel_Reservation_Prediction.git']])
        }
      }
    }
  }
}