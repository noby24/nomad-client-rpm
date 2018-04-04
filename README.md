# RPM Spec for Nomad (client mode)

Tries to follow the [packaging guidelines](https://fedoraproject.org/wiki/Packaging:Guidelines) from Fedora.

* Binary: `/usr/bin/nomad`
* Config: `/etc/nomad/`
* Shared state: `/var/lib/nomad/`
* Sysconfig: `/etc/sysconfig/nomad`

Heavily borrowed from:
https://github.com/tomhillable/consul-rpm


This RPM runs the Nomad Client daemon as root and does not create any user and group that has root privileges.

## Version

The version number is hardcoded into the SPEC.


## Build

Building it with Docker:

* Build the Docker image. Note that you must amend the `Dockerfile` header if you want a specific OS build (default is `centos7`).
    ```
    docker build -t nomad:build .
    ```

* Run the build.
    ```
    docker run -v $PWD:/RPMS nomad:build
    ```

* Retrieve the built RPMs from `$PWD`.

## Result

One RPM:
- nomad

## Run

* Install the RPM.
* Put config files in `/etc/nomad/`.
* Change command line arguments to nomad in `/etc/sysconfig/nomad`.
* Start the service and tail the logs `systemctl start nomad.service` and `journalctl -f`.
  * To enable at reboot `systemctl enable nomad.service`.

## Config

Config files are loaded in lexicographical order from the `config`. Some
sample configs are provided.

## More info

See the [nomadproject.io](http://www.nomadproject.io) website.
