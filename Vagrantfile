Vagrant.configure("2") do |config|
    master.vm.provision "shell", path: "install-docker.sh"
    config.vm.provision "shell", inline: <<-SHELL
        apt update -y
        cd /vagrant
        docker-compose pull
        docker-compose build
        docker-compose up -d
        cd ./orchestrator
        apt install python3-pip -y
        pip3 install -r requirements.txt
    SHELL
    
    config.vm.define "master" do |master|
      master.vm.box = "ubuntu/focal64"
      master.vm.hostname = "master"
      master.vm.network "private_network", ip: "10.0.0.10"
      master.vm.provider "virtualbox" do |vb|
          vb.memory = 8192
          vb.cpus = 4
      end
    end
end