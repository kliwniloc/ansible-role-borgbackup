{
  pkgs ? import <nixpkgs> { },
}:

let
  python = pkgs.python3.withPackages (ps: [
    ps.ansible
    ps.docker
    ps.molecule
    ps.molecule-plugins
    ps.pytest
    ps.pytest-testinfra
    ps.requests
  ]);
in
pkgs.mkShell {
  packages = [
    python
    pkgs.docker
    pkgs.rsync
    pkgs.python311Packages.requests
  ];

  shellHook = ''
    export ANSIBLE_ALLOW_BROKEN_CONDITIONALS=True
    export PYTHONDONTWRITEBYTECODE=1 # Keep Python from writing .pyc files


    echo "=========================================================="
    echo "🚀 Ansible Molecule Development Environment is ready"
    echo "=========================================================="
    echo "Installed Versions:"
    python --version
    ansible --version | head -n 1
    molecule --version | head -n 1
    echo "=========================================================="
    echo "Using ANSIBLE_ALLOW_BROKEN_CONDITIONALS=True for molecule-plugins/docker"
    echo "Run: molecule test -s default"
  '';
}
