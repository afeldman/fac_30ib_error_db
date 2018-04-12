# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config| 
  
  config.vm.define :rethinkdb, autostart: true, primary: true do |db|
    db.vm.box = "ubuntu/trusty64"

    db.vm.network :private_network, ip: "192.168.0.100"
    db.vm.network "forwarded_port", guest: 28015, host: 28015
    db.vm.network "forwarded_port", guest: 29015, host: 29015
    db.vm.network "forwarded_port", guest: 8080, host: 8080
    
    db.vm.provision :docker do |d|
      d.pull_images 'afeldman/rethinkdb'
      d.run 'afeldman/rethinkdb', args: "-i -t -d -p 28015:28015 -p 29015 -p 8080:8080"
    end
  end

$FLASK_SCRIPT = <<EOF
#!/usr/bin/env bash

export DB_HOST="192.168.0.100"
export FLASK_HOST="192.168.0.101"
export FLASK_APP=main.py

source /etc/lsb-release && echo "deb http://download.rethinkdb.com/apt $DISTRIB_CODENAME main" | sudo tee /etc/apt/sources.list.d/rethinkdb.list
wget -qO- http://download.rethinkdb.com/apt/pubkey.gpg | sudo apt-key add -

sudo sh -c 'apt-get update && apt-get upgrade -y'
sudo apt-get -y install python-dev python-pip rethinkdb
sudo pip install --upgrade pip
sudo pip install flask rethinkdb

cd /opt/30ib/

python bootstrap.py
python main.py
EOF
  
  config.vm.define :fac_30ib do |flask|
    flask.vm.box = "ubuntu/trusty64"
    flask.vm.network :private_network, ip: "192.168.0.101"
    flask.vm.network "forwarded_port", guest: 5000, host: 5000
    #flask.ssh.insert_key = false
    
     # the application data
    flask.vm.synced_folder ".", "/opt/30ib", type: "rsync", create: true

    flask.vm.provision :shell, inline: $FLASK_SCRIPT

  end
end
