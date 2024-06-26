def digest
def build_tag = "latest"
def poetry = new me.hhome.ImgReference(
    'harbor.hhome.me', "library/poetry310", 'latest', ''
)
podTemplate(showRawYaml: false, yaml: """
kind: Pod
spec:
  containers:
  - name: main
    image: ${poetry.digest_reference()}
    command:
    - /bin/cat
    tty: true
    volumeMounts:
      - name: cache
        mountPath: /cache
  volumes:
  - name: cache
    persistentVolumeClaim:
      claimName: poetry-cache
"""
) {
    node(POD_LABEL) {
        checkout scm
        stage('test') {
            container('main') {
                ansiColor('xterm') {
                    try {
                        sh '''
export HOME=$(pwd)
poetry config cache-dir /cache
poetry install --remove-untracked
poetry run pytest --cache-clear --junit-xml test-results.xml
'''
                    } finally {
                        junit 'test-results.xml'
                    }
                }
            }
        }
    }
}

kanikoPod() {
    checkout scm
    stage('container') {
        container('kaniko') {
            digest = kanikoBuild {
                repo = 'library/565851109_xyz'
                tag = build_tag
            }
        }
    }
}

withPod(digest) {
    checkout scm
    stage ('build') {
        container('main') {
            sh('''mkdir dist
bulletin-a --output-directory dist/
''')
        }
        zip archive: false, dir: 'dist/', glob: '', zipFile: 'site.zip'
        archiveArtifacts artifacts: 'site.zip', fingerprint: true
    }
}

awscli('jenkins--565851109-xyz') {
    stage('publish') {
        container('main') {
            when(BRANCH_NAME == 'master') {
                copyArtifacts filter: 'site.zip', fingerprintArtifacts: true, projectName: '${JOB_NAME}', selector: specific('${BUILD_NUMBER}')
                unzip zipFile: 'site.zip', dir: 'public'
                sh 'aws s3 sync public/ s3://www.565851109.xyz --exclude ".git/*" --exclude ".git*" --delete --cache-control max-age=43200'
                sh 'aws cloudfront create-invalidation --distribution-id E1ZT2KH4LRWDL8 --paths "/*"'
            }
        }
    }
}

node() {
    stage('publish-github') {
        when(BRANCH_NAME == 'master') {
            checkout scm
            gitReplicate('jenkins-565851109-xyz-github', 'git@github.com:insertjokehere/leap-second-prediction.git', 'master', 'github.com')
        }
    }
}
