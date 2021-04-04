# - Dockerfile -

jargons:
	shell ex. : RUN (shell form)
	exec ex. : RUN [“executable”, “param1”, “param2”] (exec form)

COPY - src/dest copies from the host to the docker image
ADD - same as copy but you can use a URL, you can also extract a tar file directly to the image
NOTE You can use COPY --from to copy files from previous stages, or from a separate image either local or in docker registry.

CMD - run a cmd to start your container
WORKDIR - better and cleaner cd (doesnt add a layer instead metadata to the image config. defaults to / ) performs mkdir and cd implicitly
RUN - execute command, may be exec or shell. Adds a new layer on top of the below layer. commands combined in 1 line creates 1 layer. less layer the smaller the image.
ARG  - defines parameter and default value, can be overwritten by 
--build-arg <parameter name>=<value> while bulding the image
(can be used before the FROM command but only for that)
ENV  - set environment variables. just like ARG you can override default values using --env <key>=<value> when starting your container.

ENV vs ARG
arg is for building image
env is for your future containers. you can’t change env in build time. but you can 

VOLUME - creates a folder shared by the host and container. use -v host_dest:container_dest on your run command to link.

EXPOSE and -p

a. Neither specify EXPOSE nor -p
  - If you specify neither EXPOSE nor -p, the service in the container will only be accessible from inside the container itself.

b. Only specify EXPOSE
  - If you EXPOSE a port, the service in the container is not accessible from outside Docker, but from inside other Docker containers. So this is good for inter-container communication.

c. Specify EXPOSE and -p
  - If you EXPOSE and -p a port, the service in the container is accessible from anywhere, even outside Docker.

LABEL - put descriptions and shizz

ONBUILD - special instruction to pass the commands to the next build that will mirror the base image. **This is great for making base images, to centralize boiler plate setups.

HEALTHCHECK - monitoring containers through a command.

SHELL - overrides the current shell used while building the image (linux: [“/bin/sh”, “-c”], windows: [“cmd”, “/S”]

ENTRYPOINT - run your container as an executable. commands may be written as exec or shell. It’s like shell it changes the default command w/c is for ubuntu "/bin/sh -c”. all CMD gets passed to ENTRYPOINT. to override use --entrypoint 



