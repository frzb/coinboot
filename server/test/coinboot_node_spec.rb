control "coinboot-node-1" do
  impact 1.0
  title "Coinboot node tests"
  desc "Baseline testing for Coinbot node functionality"

  describe directory('/home/ubuntu/test_dir') do
    its('property') { should cmp 'value' }
    its('owner') { should eq 'ubuntu' }
    its('group') { should eq 'ubuntu' }
  end

  describe file('/home/ubuntu/test_dir/file') do
    its('property') { should cmp 'value' }
    its('owner') { should eq 'ubuntu' }
    its('group') { should eq 'ubuntu' }
    its('content') { should match 'This is a test' }
  end

  describe command('lsb_release -d') do
    it { should exist }
    its('exit_status') { should eq 0 }
    its('stdout') { should include 'Description:	Ubuntu 20.04.4 LTS' }
  end

  describe command('uname -r') do
    it { should exist }
    its('exit_status') { should eq 0 }
    its('stdout') { should include '5.11.0-46-generic' }
  end

  describe command('zramctl') do
    it { should exist }
    its('exit_status') { should eq 0 }
    its('stdout') { should include '/dev/zram0' }
  end

end
