import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_borg_installed(host):
    cmd = host.run('/usr/local/bin/borg --version')
    assert cmd.stdout == 'borg 1.1.17'


def test_borgmatic_installed(host):
    pip_packages = host.pip_package.get_packages(
        pip_path='/etc/borgmatic/venv/bin/pip'
    )
    assert pip_packages['borgmatic']['version'] == '1.5.20'


@pytest.mark.parametrize("name, mode", [
    ('/etc/borgmatic/config.yaml', 0o600),
    ('/etc/borgmatic/hooks/error.sh', 0o700),
    ('/etc/cron.d/borgmatic', 0o644),
    ('/etc/logrotate.d/borgmatic', 0o644),
    ('/var/log/borgmatic.log', 0o644),
])
def test_config(host, name, mode):
    file = host.file(name)
    assert file.exists
    assert file.mode == mode
    assert file.user == 'root'
    assert file.group == 'root'


def test_backup(host):
    run_backup = host.run('/etc/borgmatic/venv/bin/borgmatic')
    last_archive = host.run(
        '/usr/local/bin/borg list --last 1 --short /tmp/testrepo'
    )
    archive_content = host.run(
        '/usr/local/bin/borg list /tmp/testrepo::' + last_archive.stdout
    )
    assert run_backup.rc == 0
    # note that borg lists paths without a leading slash
    assert 'etc/passwd' in archive_content.stdout
