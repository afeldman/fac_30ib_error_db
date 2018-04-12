# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"
  
  config.vm.define :rethinkdb, autostart: true, primary: true do |db|
    db.vm.network :private_network, ip: "192.168.33.39"
    db.vm.network "forwarded_port", guest: 28015, host: 28015
    db.vm.network "forwarded_port", guest: 8080, host: 8080
    
    db.vm.provision :docker do |d|
      d.pull_images 'afeldman/rethinkdb'
      d.run 'afeldman/rethinkdb', args: "-i -t -d -p 28015:28015 -p 29015 -p 8080:8080"
    end
  end

  config.vm.define :fac_30ib do |flask|
     # the application data
    flask.vm.synced_folder ".", "/opt/30ib", type: "rsync", create: true

 #   flask.vm.box = "geerlingguy/ubuntu1604"
    flask.vm.network :private_network, ip: "192.168.33.39"
    flask.ssh.insert_key = false

    flask.vm.provision :shell, inline: 'export DB_HOST="192.168.33.39"'
  end
end
