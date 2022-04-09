# Please always use the cookstyle linter
control 'coinboot-plugin-endpoint' do
  impact 1.0
  title 'Coinboot server plugin HTTP endpoint'
  desc 'Verify the Coinboot server plugin HTTP endpoint is available'

  describe http('http://192.168.1.2/plugins/') do
    its('status') { should cmp 200 }
    its('body') { should include 'coinboot_test-plugin_v0.0.1' }
  end
end
control 'coinboot-plugin' do
  impact 1.0
  title 'Coinboot node plugin file structure'
  desc 'Verify plugin file structure on the Coinboot worker node'

  describe directory('/home/ubuntu/test_dir') do
    its('owner') { should eq 'ubuntu' }
    its('group') { should eq 'ubuntu' }
  end

  describe file('/home/ubuntu/test_dir/file1') do
    its('owner') { should eq 'ubuntu' }
    its('group') { should eq 'ubuntu' }
    its('content') { should match 'This is a test' }
  end
end

control 'coinboot-kernel' do
  impact 1.0
  title 'Coinboot node Kernel version'
  desc 'Verify the Kernel version running on the Coinboot worker node'

  describe command('uname -r') do
    its('exit_status') { should eq 0 }
    its('stdout') { should include '5.11.0-46-generic' }
  end
end

control 'coinboot-distribution' do
  impact 1.0
  title 'Coinboot node Distribution release'
  desc 'Verify the distribution release running on the Coinboot worker node'

  describe command('lsb_release -d') do
    its('exit_status') { should eq 0 }
    its('stdout') { should include 'Description:	Ubuntu 20.04.4 LTS' }
  end
end

control 'coinboot-zram' do
  impact 1.0
  title 'Coinboot node ZRAM RAM Compresssion'
  desc 'Verify the ZSTD compressed ramdrive used for the RootFS'

  describe command('zramctl') do
    its('exit_status') { should eq 0 }
    its('stdout') { should include '/dev/zram0' }
  end
end
