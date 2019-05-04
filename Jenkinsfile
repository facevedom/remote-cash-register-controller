node {

    def python = 'python3'
    def pip = 'pip3'

    stage ('Checkout') {
        git branch: 'develop', 
            url: 'https://github.com/facevedom/remote-cash-register-controller'
    }

    stage ('Fetch dependencies') {
        sh "${pip} install requirements.txt"
    }

    stage ('Test') {
        dir('cash_register_closer') {
            sh "${python} test.py"
        }
    }

    stage('test') {
        try {
            sh '${python} test.py'
        } catch (e) {
            error 'Unit tests failed'
        } finally {
            junit 'test-reports/*.xml'
        }
    }
}