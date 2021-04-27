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
