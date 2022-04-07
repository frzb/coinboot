# Please always use the cookstyle linter
control 'coinboot-plugin' do
  impact 1.0
  title 'Coinboot node tests'
  desc 'Baseline testing for Coinbot node functionality'

  describe directory('/home/ubuntu/test_dir') do
    its('owner') { should eq 'ubuntu' }
    its('group') { should eq 'ubuntu' }
  end

  describe file('/home/ubuntu/test_dir/file') do
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