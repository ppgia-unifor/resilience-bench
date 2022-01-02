Vagrant.configure("2") do |config|
    
    config.vm.synced_folder "~/.aws", "/home/vagrant/.aws"

    config.vm.define "master" do |master|
      master.vm.box = "ubuntu/focal64"
      master.vm.hostname = "master"
      master.vm.network "private_network", ip: "10.0.0.10"
      master.vm.provider "virtualbox" do |vb|
          vb.memory = 16384
          vb.cpus = 8
      end
      # prepare ubuntu
      master.vm.provision "shell", inline: <<-SHELL
        apt update -y
        apt install -y apt-transport-https ca-certificates curl gnupg lsb-release
      SHELL

      # install docker
      master.vm.provision "shell", inline: <<-SHELL
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
        echo \
          "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
          $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
        apt update -y
        apt install docker-ce docker-ce-cli containerd.io -y

        systemctl enable docker
        systemctl daemon-reload
        systemctl restart docker

        curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        chmod +x /usr/local/bin/docker-compose

        usermod -aG docker $USER
        newgrp docker
      SHELL

      # install applications
      master.vm.provision "shell", inline: <<-SHELL
        nohup ./git-repo-watcher/git-repo-watcher -d ${PWD} < /dev/null &
        cd /vagrant
        docker rm -f $(docker ps -a -q)
        docker-compose down
        docker-compose pull
        docker-compose build --no-cache
        docker-compose up -d
      SHELL
    end
end