
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out CampusCare source code'
                checkout scm
            }
        }

        stage('Check Python') {
            steps {
                bat 'py --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'py -m venv .venv'
                bat '.venv\\Scripts\\python -m pip install -r requirements.txt'
            }
        }

        stage('Run Automated Tests') {
            steps {
                bat '.venv\\Scripts\\python -m unittest discover -s tests -v'
            }
        }
    }

    post {
        success {
            echo 'CampusCare CI pipeline completed successfully!'
        }
        failure {
            echo 'CampusCare CI pipeline failed. Check the console output.'
        }
    }
}

