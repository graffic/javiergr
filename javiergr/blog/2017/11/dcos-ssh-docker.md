title: SSH on a DCOS+Marathon cluster with Docker
date: 2017-11-04
category: technical
published: true
summary: I just wanted to test some latencies from a DCOS cluster.

I just wanted to test some latencies from a DCOS cluster.

The first suggestion to run some commands in an existing container comes from [DCOS documentation](https://dcos.io/docs/1.10/monitoring/debugging/task-exec/) and is `dcos task exec`. But it only works for containers launched using the [Universal Container Runtime](https://dcos.io/docs/1.10/deploying-services/containerizers/ucr/). The second suggestion, if your nodes run docker, is to [SSH into the nodes](https://dcos.io/docs/1.10/administering-clusters/sshcluster/#docs-article) and then `docker exec ` a shell in a container to do some tests. Although this means you need to have access to the nodes themselves (private key/password), something a sysadmin won't give you without a very good reason.

## El cheapo attempt.

If you have access to the dcos cluster you can always start a new app using the [DCOS cli tool](https://dcos.io/docs/1.10/cli/). An app with only one container with ssh, curl, and your public ssh key in `authorized_keys`.

    :::docker
    FROM alpine:latest

    RUN apk --no-cache add openssh curl && \
        ssh-keygen -A

    COPY authorized_keys /root/.ssh/authorized_keys

    ENTRYPOINT ["/usr/sbin/sshd", "-De"]
    

Publish it somewhere on the public internet (I used the public docker registry at [hub.docker.com](https://hub.docker.com)). And prepare a new task file (`task.json`) to launch it. This task has the id `staging-authentication-latencies` that we will use later.

    :::json
    {
        "id": "staging-authentication-latencies",
        "container": {
            "type": "DOCKER",
            "docker": {
            "image": "docker.io/graffic/ssh:latest",
            "network": "BRIDGE",
            "portMappings": [
                    {
                        "hostPort": 22022,
                        "containerPort": 22,
                        "protocol": "tcp"
                    }
            ],
            "privileged": false,
            "force_pull_image": true
            }
        },
        "instances": 1,
        "cpus": 0.5,
        "mem": 512
    }

Now we can:

* Start the new app with `dcos marathon app add task.json`
* See how the deploy is going: `dcos marathon app show staging-authentication-latencies`

Find the `task` entry and get the `host` IP. You will need that to connect via ssh:

    :::json
    {
        "tasks": [
            {
            "appId": "/staging-authentication-latencies",
            "host": "X.X.X"
            }
        ]
    }

* SSH into the container: `ssh -p 22022 root@host_you_got_from_app_show` and run your tests from there.
* Remove the app when you're done: `dcos marathon app remove staging-authentication-latencies`
