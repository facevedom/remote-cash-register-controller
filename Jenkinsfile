node {

    def python = 'python3'
    def pip = 'pip3'

    stage ('Checkout') {
        cleanWs()
        
        git branch: 'develop', 
            url: 'https://github.com/facevedom/remote-cash-register-controller'
    }

    stage ('Fetch dependencies') {
        sh "${pip} install -r requirements.txt"
    }

    stage('Test') {
        try {
            dir('cash_register_closer') {
                sh "${python} test.py"
            }
        } catch (e) {
            error 'Unit tests failed'
        } finally {
            junit 'test-reports/*.xml'
        }
    }
}