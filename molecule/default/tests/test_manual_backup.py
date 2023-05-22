import pytest

testinfra_hosts = ['borg-client']


compression_types = [
    'none',
    'lz4',
    'zstd',
    'zstd,10',
    'zlib',
    'zlib,6',
]


"""Creates backups with all possible combinations of compression to the backup
host"""
@pytest.mark.parametrize('compression', compression_types)
def test_backup_push(host, compression):
    c = host.run(f'borg create -C "{compression}" borg@borg-server:/opt/borg/borg-client::testinfra-{{now:%S.%f}} /etc')
    assert c.rc == 0
    assert c.stdout == ''
    assert c.stderr == ''


@pytest.mark.parametrize('compression', compression_types)
def test_backup_restore(host, compression):
    # Create backup
    c = host.run(f'borg create -C "{compression}" borg@borg-server:/opt/borg/borg-client::testinfra-backup-restore-{compression} /var')
    assert c.rc == 0
    assert c.stdout == ''
    assert c.stderr == ''

    # Restore Backup
    c = host.run(f'cd /mnt && borg extract borg@borg-server:/opt/borg/borg-client::testinfra-backup-restore-{compression}')
    assert c.rc == 0
    assert c.stdout == ''
    assert c.stderr == ''

    # Check if every file exists, content has, and permissions / metadata
    c1 = host.run('cd /var && find /var -type f -printf "%P\n" | sort | xargs -i sh -c "echo {}; sha512sum {} | cut -d \' \' -f 1; ls -l {}; echo"')
    c2 = host.run('cd /mnt/var && find /var -type f -printf "%P\n" | sort | xargs -i sh -c "echo {}; sha512sum {} | cut -d \' \' -f 1; ls -l {}; echo"')
    assert c1.rc == 0 and c2.rc == 0
    assert c1.stderr == '' and c2.stderr == ''
    assert c1.stdout == c2.stdout

    # Delete directory extract directory again for future tests
    c = host.run('rm -rf /mnt/var')
    assert c.rc == 0
    assert c.stdout == ''
    assert c.stderr == ''

    # Delete backup
    c = host.run(f'borg delete borg@borg-server:/opt/borg/borg-client::testinfra-backup-restore-{compression}')
    assert c.rc == 0
    assert c.stdout == ''
    assert c.stderr == ''
