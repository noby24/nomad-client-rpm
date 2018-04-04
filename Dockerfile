# default build is for CentOS7, change the base image to fit your build.
FROM centos:centos7

RUN yum update -y
RUN yum install -y rpmdevtools mock

RUN cd /root && rpmdev-setuptree
ADD SOURCES/* /root/rpmbuild/SOURCES/
ADD SPECS/* /root/rpmbuild/SPECS/
RUN ln -s /root/rpmbuild/RPMS /RPMS

VOLUME ["/RPMS"]

CMD set -x && cd /root && spectool -g -R rpmbuild/SPECS/nomad.spec && rpmbuild -ba rpmbuild/SPECS/nomad.spec
