require 'socket'

$coinboot_docker = <<SCRIPT

if ! docker info; then
  curl -fsSL get.docker.com -o get-docker.sh
  sudo sh get-docker.sh
  sudo usermod -aG docker vagrant
fi

if ! docker-compose; then
  sudo curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
  sudo chmod +x /usr/local/bin/docker-compose
fi

docker-compose -f /vagrant/docker-compose.yml up -d --build --force-recreate

# Configure forwading and NAT cause the DHCP server vagrant box acts currently
# also as gateway.
# Ignore the masquerading set up for Docker (destination 172.17.0.0/16).
if ! iptables -L -t nat | grep -q 'MASQUERADE  all  --  anywhere'; then
  iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
else
  echo 'Masquerading iptables rule already set.'
fi

# FIXME: Using a default policy seems a little bit coarse.
sudo iptables -P FORWARD ACCEPT

SCRIPT

Vagrant.configure(2) do |config|
  # Dynamically allign number of core of the VMs with the host
  # to speed up things as much as possible.
  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--cpus", `#{RbConfig::CONFIG['host_os'] =~ /darwin/ ? 'sysctl -n hw.ncpu' : 'nproc'}`.chomp]
    vb.customize ["modifyvm", :id, "--memory", 2048]
  end

  config.vm.define "client" do |machine|
    # machine.vm.box = "bento/ubuntu-16.04"
    # FIXME: Built own empty Vagrantbox
    machine.vm.box = "c33s/empty"
    machine.vm.hostname = "client"
    machine.ssh.host = "192.168.1.23"
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
                    "--boot1", "net"]
      # Set up serial port
      # name = /dev/ttyS0
      # IO address = 0x3F8
      # Interupt Request (IRQ) = 4
      # Use with: socat -d -d /tmp/serial_port_client PTY
      vb.customize ["modifyvm", :id, "--uart1", "0x3f8", "4"]
      vb.customize ["modifyvm", :id, "--uartmode1", "server", "/tmp/serial_port_client"]
      vb.customize ["modifyvm", :id, "--memory", "2048"]
    end
  end

  config.vm.define "coinboot-server" do |machine|
    machine.vm.box = "bento/ubuntu-16.04"
    machine.vm.provision "shell", inline: $coinboot_docker
    interfaces = []

    Socket.getifaddrs.each do |addr_info|
      interfaces.push(addr_info.name)
    end

   # FIXME: We need to detect if an interface is not only present
   # but also if it is in the state "UP" to avoid false positives.
    if interfaces.uniq.include?('eth1')
      machine.vm.network "public_network", ip: "192.168.1.2",
        bridge: ['eth1']
    elsif interfaces.uniq.include?('enx00e04c680379')
      machine.vm.network "public_network", ip: "192.168.1.2",
        bridge: ['enx00e04c680379']
    else
      machine.vm.network "private_network", ip: "192.168.1.2"
    end
        # Using '82540EM' provides 1GBit/s interface not just the default
        # 100MBit/s one.
    machine.vm.provider "virtualbox" do |vb|
      vb.customize ['modifyvm', :id, '--nictype2', '82540EM']
    end
  end
end
