require 'socket'

$coinboot_docker = <<SCRIPT
COMPOSEFILE=/vagrant/docker-compose.yml

if ! docker info; then
  curl -fsSL get.docker.com -o get-docker.sh
  sudo sh get-docker.sh
  sudo usermod -aG docker vagrant
fi

if ! which docker-compose; then
  sudo curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
  sudo chmod +x /usr/local/bin/docker-compose
fi

if ! docker plugin ls |grep -q loki; then
  docker plugin install grafana/loki-docker-driver:latest --alias loki --grant-all-permissions
  docker plugin ls
fi

# Configure forwading and NAT cause the DHCP server vagrant box acts currently
# also as gateway.
# Ignore the masquerading set up for Docker (destination 172.17.0.0/16).
if ! iptables -L -t nat | grep -q 'MASQUERADE  all  --  anywhere'; then
  iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
else
  echo 'Masquerading iptables rule already set.'
fi

# enable Password login to Vagrant box for remote debugging of VMs
sudo sed -i "s/.*PasswordAuthentication.*/PasswordAuthentication yes/g" /etc/ssh/sshd_config
sudo systemctl restart ssh

# FIXME: Using a default policy seems a little bit coarse.
sudo iptables -P FORWARD ACCEPT

SCRIPT


Vagrant.configure(2) do |config|
  # Dynamically allign number of core of the VMs with the host
  # to speed up things as much as possible.
  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--cpus", `#{RbConfig::CONFIG['host_os'] =~ /darwin/ ? 'sysctl -n hw.ncpu' : 'nproc'}`.chomp]
    vb.customize ["modifyvm", :id, "--memory", 3096]
    vb.customize ["modifyvm", :id, "--nicpromisc2", "allow-all"]
  end

  config.vm.define "coinboot-server" do |machine|
    machine.vm.box = "bento/ubuntu-20.04"
    machine.vm.hostname = "coinboot-server"
    machine.vm.provision "shell", inline: $coinboot_docker
    machine.vm.provision "shell", inline: "/vagrant/server/run_coinboot", env: {"KERNEL": "5.4.0-58-generic"}
    # Port-forwarding for Grafana
    machine.vm.network "forwarded_port", guest: 3000, host: 3000
    # Port-forwarding for VNC of Qemu/KVM
    machine.vm.network "forwarded_port", guest: 5900, host: 5900
    interfaces = []

    Socket.getifaddrs.each do |addr_info|
      interfaces.push(addr_info.name)
    end

   # FIXME: We need to detect if an interface is not only present
   # but also if it is in the state "UP" to avoid false positives.
   # Also take care that the Coinboot plugin archive for the client
    # acting as proper VagrantBox is only loaded when we not use a physical client a.k.a.
    # real hardware.
    if interfaces.uniq.include?('eth1')
      machine.vm.network "public_network", ip: "192.168.1.2",
        bridge: ['eth1']
      puts "Using interface eth1 as bridge interface"
      machine.vm.provision "shell", inline: 'rm -fv /vagrant/plugins/coinboot-vagrantbox.tar.gz'
    elsif interfaces.uniq.include?('enx00e04c680379')
      machine.vm.network "public_network", ip: "192.168.1.2",
        bridge: ['enx00e04c680379']
      machine.vm.provision "shell", inline: 'rm -fv /vagrant/plugins/coinboot-vagrantbox.tar.gz'
      puts "Using interface enx00e04c680379 as bridge interface"
    else
      # No IP address is configured, this is handled by the "run_coinboot" script.
      # We have to configure an IP even if auto_config is set to true, else same sanity checks of Vagrant
      # are not happy.
      machine.vm.network "private_network", ip: "192.168.1.2", auto_config: false
      puts "Using interface vboxnet_pxe as bridge interface"
      # FIXME: Path has changed in monorepo
      # machine.vm.provision "shell", inline: 'cp -v /vagrant/example_plugins/builds/coinboot-vagrantbox.tar.gz /vagrant/plugins/coinboot-vagrantbox.tar.gz'
    end
        # Using '82540EM' provides 1GBit/s interface not just the default
        # 100MBit/s one.
    #machine.vm.provider "virtualbox" do |vb|
    #  vb.customize ['modifyvm', :id, '--nictype2', '82540EM']
  end

  config.vm.define "worker" do |machine|
    machine.vm.box = "clink15/pxe"
    machine.vm.hostname = "worker"
    machine.ssh.host = "192.168.1.10"
    machine.ssh.port = 22
    machine.ssh.password = "ubuntu"
    machine.ssh.username = "ubuntu"
    # Switch to rsync for syncing files to Vagrantbox caused by the initial
    # lack of the Virtualbox guest extension.
   # machine.vm.synced_folder "./plugins", "/vagrant", type: "rsync"
    machine.vm.provider "virtualbox" do |vb|
    # for loop instead of each loop.
    # Because for does not create a new scope like each does.
    # New scope is bad cause we need the variable
    # vboxnet_pxe afterwards.
    for addr_info in Socket.getifaddrs
      if addr_info.addr.ipv4?
        if addr_info.addr.ip_address.eql? "192.168.1.1"
          vboxnet_pxe = addr_info.name
          puts "Internal network for TFTP/PXE: #{vboxnet_pxe}"
        end
      end
    end
      vb.customize ["modifyvm", :id,
                    "--nic1", "hostonly",
                    "--hostonlyadapter1", vboxnet_pxe,
                    "--macaddress1", "080027C1447D",
	            "--nictype1", "82540EM",
                    "--boot1", "net"]
      # Set up serial port
      # name = /dev/ttyS0
      # IO address = 0x3F8
      # Interupt Request (IRQ) = 4
      # Use with: socat -d -d /tmp/serial_port_client PTY
      vb.customize ["modifyvm", :id, "--uart1", "0x3f8", "4"]
      vb.customize ["modifyvm", :id, "--uartmode1", "server", "/tmp/serial_port_worker"]
      vb.customize ["modifyvm", :id, "--memory", "2048"]
    end
  end

  config.vm.define "worker_without_pxe_firmware" do |machine|
    # Using ubuntu/focal cause it is not using LVM.
    # LVM and grubenv is not working as expected.
    machine.vm.box = "ubuntu/focal64"
    machine.vm.hostname = "client-no-pxe-firmware"
    #machine.ssh.host = "192.168.1.11"
    #machine.ssh.port = 22
    #machine.ssh.password = "vagrant"
   # machine.ssh.username = "vagrant"
    # Switch to rsync for syncing files to Vagrantbox caused by the initial
    # lack of the Virtualbox guest extension.
    # machine.vm.synced_folder "./plugins", "/vagrant", type: "rsync"
    machine.vm.provision "shell", /vagrant/scripts/set_up_grub_ipxe_chainloading
    machine.vm.provision "shel", sudo reboot_with_iPXE
    machine.vm.provision "shel", sudo reboot
    for addr_info in Socket.getifaddrs
      if addr_info.addr.ipv4?
        if addr_info.addr.ip_address.eql? "192.168.1.1"
          vboxnet_pxe = addr_info.name
          puts "Internal network for TFTP/PXE: #{vboxnet_pxe}"
        end
      end
    end
    # We have to configure an IP even if auto_config is set to true, else same sanity checks of Vagrant
    # are not happy.
    machine.vm.network "private_network", ip: "192.168.1.20", auto_config: false, name: vboxnet_pxe
    machine.vm.provider "virtualbox" do |vb|
      #vb.customize ["modifyvm", :id,
      #              "--nic1", "intnet",
      #              "--macaddress1", "080027C1447E"
      #]
      vb.customize ["modifyvm", :id, "--memory", "2048"]
    end
  end
end
