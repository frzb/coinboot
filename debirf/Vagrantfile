# Copyright (C) 2018 Gunter Miegel coinboot.io
#
# This file is part of Coinboot.
#
# Coinboot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


environment = {
'DEBIRF_KERNEL' => '5.0.0-13-generic',
'DEBIRF_SUITE' => 'disco',
'RELEASE' => '$(date +"%Y%m%d")',
'VERSION' => '0.98 Beta'
}

Vagrant.configure(2) do |config|
  # Dynamically allign number of core of the built VM with the host
  # to speed up things as much as possible.
  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--cpus", `#{RbConfig::CONFIG['host_os'] =~ /darwin/ ? 'sysctl -n hw.ncpu' : 'nproc'}`.chomp]
    vb.customize ["modifyvm", :id, "--memory", 2048]
  end

  config.vm.define "make-rootfs" do |machine|
  machine.vm.box = "ubuntu/xenial64"
  machine.vm.hostname = "make-rootfs"
  machine.vm.synced_folder "./", "/mnt"
  # FIXME: Have a look at this Kernel version issue in general.
  # Take care that the built box is running on the most recent kernel.
  # For that we have to reboot the Vagrant box which is achieved by
  # the reload-plugin.
  #config.vm.provision "shell", inline: 'apt update; apt dist-upgrade --yes'
  config.vm.provision "shell", inline: 'apt update; apt upgrade --yes'
  config.vm.provision "shell", inline: 'source /vagrant/profiles/coinboot/debirf.conf && apt install linux-image-$DEBIRF_KERNEL --yes'
  config.vm.provision :reload
  config.vm.provision "shell", inline: 'env && /mnt/create_rootfs_and_kernel', env: environment
  # Dynamically allign number of core of the built VM with the host
  # to speed up things as much as possible.
  end
end

