# Linux Privilege Escalation

This repository contains content delivered as part of a workshop at AusCERT 2020. It includes:

* A Dockerfile used to build a Docker containers to facilitate practical exercises
* A Python script used to configure the practical exercises within these containers

## Installing Docker

To install Docker on your chosen operating system, consult the [Docker documentation](https://docs.docker.com/get-docker/).

## Setting up the Docker image

From the root of the Git repository (the same directory as where this `README.md` file is stored), run the following command:

```docker image build -t sudochop/privesc docker/```

(Note the `-t sudochop/privesc` above isn't required, but tagging the image makes it slightly easier to refer to in subsequent commands!).

Docker will take a few minutes to download the relevant base image and configure it to our needs. If the build was successful, you should see message similar to the below:

```Successfully built <id>
Successfully tagged sudochop/privesc:latest```

If you list your Docker images, you should also see the newly-built image present:

```docker image ls```

## Creating and Running a Docker container

Now we have our image, we need to create and run a container on top of that image we can interact with:

```docker run -d --name linuxprivesc -p <port>:22 sudochop/privesc```

In the above command, choose a `<port>` which is not currently bound as a listener; we will be using this port to SSH into the container. One such port might be TCP 2222 for example:

```docker run -d --name linuxprivesc -p 2222:22 sudochop/privesc```

Docker will spit out a long ID value if the container is created successfully. We should also be able to see our new container:

```docker container ls```

## Configuring practical exercises

With your Docker container set up and running, you should be able to SSH into the container as the `lowpriv` user (password is 'lowpriv'):

```ssh -p <port> lowpriv@localhost ```

In the user's home directory, there should be an executable named '`config-privescs`'. Run this binary, which will display a menu allowing you to choose whichever practical exercise you wish to configure, as well as its difficulty:

```./config-privescs``` 

## Rolling-back a practical exercise

## Removing a Docker container

Once you're done with our container, exit SSH back to your command line environment.

We first need to stop our container. `linuxprivesc` below refers to the same `--name` value we gave with our `docker run` command above. If you used a different value, use your chosen value below instead:

```docker container stop linuxprivesc```

We can then remove the container (again, with the same `--name` caveat as above):

```docker container rm linuxprivesc```

If you also want to remove the image we created previously:

```docker image rm sudochop/privesc```

## Troubleshooting

### SSH 'Host key verification failed.'

If you remove the image, then create a new image and subsequent containers in the same manner and attempt SSH on the same port, you may receive an error that states something similar to the below:

```ECDSA host key for [localhost]:2222 has changed and you have requested strict checking.
Host key verification failed.```

This is basically due to the Docker image build script regenerating SSH keys on each creation. As these have now changed, we need to tell our host to forget about the old key:

```ssh-keygen -R [localhost]:<port>```

Your `<port>` value is dependent upon what was configured during your container creation process. In the above error, for example, this is port 2222. Run the above command, and then attempt SSH again and you should be good.