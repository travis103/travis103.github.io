FROM harbor.local.hqq.com/hqq/ansible:alpine3

WORKDIR /tmp
COPY  .  /tmp

# ==> Creating inventory file...
# RUN echo localhost > inventory

# ==> Executing Ansible...

# RUN ansible-playbook -i inventory repos-update.yml \
#      --connection=local --sudo

ENTRYPOINT ["ansible-playbook","-i","inventory"]
CMD ["repos-update.yml"]
