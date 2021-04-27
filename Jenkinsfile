def digest
def build_tag = uniqueTag()

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
            sh('''#!/bin/bash -e
mkdir dist
python bulletin-a.py
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
            }
        }
    }
}

node() {
    stage('publish-github') {
        checkout scm
        withCredentials([
            sshUserPrivateKey(
                credentialsId: 'jenkins-willhughes-name-github',
                keyFileVariable: 'SSH_KEYFILE',
                passphraseVariable: '',
                usernameVariable: ''
            )
        ]) {
            sh '''
mkdir ~/.ssh
chmod 0700 ~/.ssh
ssh-keyscan github.com > ~/.ssh/known_hosts
echo "IdentityFile ${SSH_KEYFILE}" > ~/.ssh/config
git remote add github git@github.com:insertjokehere/leap-second-prediction.git
git push -f github $(git rev-parse HEAD):master'''
        }
    }
}
