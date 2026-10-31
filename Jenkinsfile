pipeline {
    agent any

    environment {
        VENV_DIR = ".venv"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install dependencies') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'python3 -m venv .venv'
                        sh '.venv/bin/python -m pip install --upgrade pip'
                        sh '.venv/bin/python -m pip install -r requirements.txt'
                    } else {
                        bat 'py -m venv .venv'
                        bat '.venv\\Scripts\\python -m pip install --upgrade pip'
                        bat '.venv\\Scripts\\python -m pip install -r requirements.txt'
                    }
                }
            }
        }

        stage('Automated tests') {
            steps {
                script {
                    if (isUnix()) {
                        sh '.venv/bin/python -m unittest discover -s tests -v'
                    } else {
                        bat '.venv\\Scripts\\python -m unittest discover -s tests -v'
                    }
                }
            }
        }

        stage('Build Docker image') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'docker build -t campuscare:latest .'
                    } else {
                        bat 'docker build -t campuscare:latest .'
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'CampusCare pipeline completed: tests passed and Docker image built.'
        }
        failure {
            echo 'CampusCare pipeline failed. Review the stage logs and fix the issue.'
        }
    }
}
