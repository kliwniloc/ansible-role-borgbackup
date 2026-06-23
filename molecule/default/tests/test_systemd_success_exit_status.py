testinfra_hosts = ["borg-client", "borg-client-success-exit-status"]


def test_systemd_service_success_exit_status(host):
    service = host.file("/etc/systemd/system/borg_backup@borg-server.service")

    assert service.exists

    if host.backend.get_hostname() == "borg-client-success-exit-status":
        assert service.contains(r"^SuccessExitStatus=1 TEMPFAIL$")
    else:
        assert not service.contains(r"^SuccessExitStatus=")
