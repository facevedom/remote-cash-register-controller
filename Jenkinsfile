node {
    def python = 'python3'
    def pip = 'pip3'
    def src_dir = 'cash_register_closer'

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
            dir("${src_dir}") {
                sh "${python} test.py"
            }
        } catch (e) {
            error 'Unit tests failed'
        } finally {
            junit "${src_dir}/test-reports/*.xml"
        }
    }

    // increase version with build
    stage('Build') {
        sh 'mkdir dist'
        sh "sed -i -e "s/##BUILD##/${env.BUILD_NUMBER}/g" config.ini"
        sh "tar vpczf dist/dist.tar.gz --exclude='dist' --exclude='Jenkinsfile*' --exclude='__pycache__'  --exclude='*@tmp' --exclude='.[^/]*' ."
        archiveArtifacts artifacts: 'dist/dist.tar.gz', fingerprint: true, onlyIfSuccessful: true
    }
}