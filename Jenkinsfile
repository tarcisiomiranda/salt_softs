// DOC: https://plugins.jenkins.io/ssh-steps/#plugin-content-remote

def syndics = [
    'TMM' : ['192.168.29.30', 22, 'OUT'],
    'XTK' : ['192.168.29.40', 22, 'XTK'],
]

def remote = [:]
def passwd = ""

pipeline {
    agent any 
    stages {
        stage('Verificando se o ambiente é de homologação ou produção...') {
            steps { 
                script {
                    if(env.SALT_SOFTS_DEBUG){
                        if (env.SALT_SOFTS_DEBUG.toLowerCase() == 'true') {
                            print "|---> Rodando em modo de Desenvolvimento <---|"
                            syndics = [
                                'DEV' : ['192.168.29.30', 19999, 'OUT'],
                                'XTK' : ['192.168.29.40', 22, 'XTK'],
                            ]
                        }

                    } else {
                        print "|---> Rodando em Produção... <---|"
                    }
                }
            }
        }

        stage('Get password for login in XTK Host') {
            steps { 
                script {
                    if(env.PASSWD_JEKINS){
                        passwd = PASSWD_JEKINS
                        print "|---> One-line String Parameter <---|"
                        print "PASSWD SVC_JENKINS_LOCAL: ${passwd}"
                    }
                }
            }
        }

        stage('Start get updates data in salt syndic') {
            steps {
                script {
                    print "SYNDICS A SEREM EXECUTADOS: ${syndics}"
                    syndics.each{ SYNDIC,IPV4 ->
                        // connection
                        remote.name = SYNDIC
                        remote.host = IPV4[0]
                        remote.port = IPV4[1]
                        remote.user = "svc.jenkins.local"
                        remote.timeoutSec = 120
                        remote.allowAnyHosts = true
                        remote.password = passwd
                        // remote.sudo = true
                        // remote.identityFile = "/var/jenkins_home/.ssh/id_rsa"

                        if (IPV4[2].toLowerCase() == 'xtk') {
                            print "| ------------> Using  XTK <------------- |"
                            sh "rm -f ${SYNDIC}.json ${SYNDIC}_update.json"
                            print "| --> The old files have been removed <-- |"
                            sshCommand remote: remote, command: "sudo mkdir -p /srv/salt/srv/salt/jenkins_temp/" + JOB_NAME
                            // Ajustando permissao do svc.jenkins.local
                            sshCommand remote: remote, command: "sudo chown svc.jenkins.local:svc.jenkins.local /srv/salt/srv/salt/jenkins_temp/" + JOB_NAME
                            sshPut remote: remote, from: 'get_soft.py', into: "/srv/salt/srv/salt/jenkins_temp/" + JOB_NAME + "/get_soft.py"
                            sshCommand remote: remote, command: "sudo docker exec saltstack python3 /srv/salt/jenkins_temp/" + JOB_NAME + \
                            "/get_soft.py -b -s " + SYNDIC
                            sshGet remote: remote, from: "/srv/salt/srv/salt/jenkins_temp/" + JOB_NAME + "/" + SYNDIC + ".json", into: "./" + SYNDIC + ".json", override: true

                            // sh "python3.9 mysql_addon.py ${SYNDIC}.json"

                        } else {
                            print "| ------------> Using SALT <------------- |"
                            sh "rm -f ${SYNDIC}.json ${SYNDIC}_update.json"
                            print "| --> The old files have been removed <-- |"
                            sshCommand remote: remote, command: "sudo mkdir -p /tmp/" + JOB_NAME
                            // Ajustando permissao do svc.jenkins.local
                            sshCommand remote: remote, command: "sudo chown svc.jenkins.local:svc.jenkins.local /tmp/" + JOB_NAME
                            sshPut remote: remote, from: 'get_soft.py', into: "/tmp/" + JOB_NAME + "/get_soft.py"
                            sshCommand remote: remote, command: "sudo /usr/bin/python3 /tmp/" + JOB_NAME + \
                            "/get_soft.py --get-hotfix > /tmp/" + JOB_NAME + "/" + SYNDIC + ".json"
                            sshGet remote: remote, from: "/tmp/" + JOB_NAME + "/" + SYNDIC + ".json", into: "./" + SYNDIC + ".json", override: true

                            // sh "python3.9 mysql_addon.py ${SYNDIC}.json"
                        }
                    }
                }
            }
        }
    }
}
