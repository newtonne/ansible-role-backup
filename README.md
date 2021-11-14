Ansible Role: Backup
====================

[![CI](https://github.com/newtonne/ansible-role-backup/workflows/CI/badge.svg?event=push)](https://github.com/newtonne/ansible-role-backup/actions?query=workflow%3ACI)

Installs and configures [borgmatic](https://github.com/witten/borgmatic) and [borg](https://www.borgbackup.org), for automated backup of files, as well as MySQL and PostgreSQL databases.

Requirements
------------

Optional requirements:

* `cron` must be installed in order to automate the backups.

* MySQL or a MySQL-compatible database must be installed in order to backup MySQL databases. Similarly for PostgreSQL databases.

Role Variables
--------------

Available variables are listed below, along with default values (see defaults/main.yml):

### Borgmatic config-related

```
backup_directories: []
```
The list of directories (or individual files) to backup.

```
backup_mysql_databases: []
```
The list of MySQL databases to backup. See [borgmatic - database dump hooks](https://torsion.org/borgmatic/docs/how-to/backup-your-databases/#database-dump-hooks) for more info.

```
backup_postgresql_databases: []
```
The list of PostgreSQL databases to backup. See [borgmatic - database dump hooks](https://torsion.org/borgmatic/docs/how-to/backup-your-databases/#database-dump-hooks) for more info.

```
backup_repositories: []
```
The list of `borg` repositories to backup to. These must be created in advance using [`borg init`](https://borgbackup.readthedocs.io/en/stable/usage/init.html). Also see [borg documentation on repository URLs](https://borgbackup.readthedocs.io/en/stable/man_intro.html?highlight=ssh%3A%2F%2F#repository-urls).

```
backup_location_options: {}
backup_storage_options: {}
backup_retention_options: {}
backup_consistency_options: {}
backup_hooks_options: {}
```
These variables can be used to supply extra configuration to `borgmatic`, such as the encryption passphrase for the `borg` repo or additional/alternative hook scripts/commands. See the [borgmatic schema](https://projects.torsion.org/borgmatic-collective/borgmatic/src/tag/1.5.20/borgmatic/config/schema.yaml) for the complete list of config options.

```
backup_hooks_globlist: hooks/*
```
The glob patterns that the fileglob lookup will use to find hook scripts on the control machine.

```
backup_hooks_directory: /etc/borgmatic/hooks
```
The directory to which any `borgmatic` hook scripts found by the above glob patterns will be copied.

### General

```
backup_cron_jobs
  - schedule: "0 3 * * *"
#   action: create
```
The list of cron time specifications and actions to perform. If no action is specified, `borgmatic` will perform all actions, that is, prune, create and check (see [borgmatic docs - set up backups](https://torsion.org/borgmatic/docs/how-to/set-up-backups/#backups)). If set to blank, no crontab will be configured.

```
backup_cron_path: "{{ backup_borg_path | dirname }}:/usr/bin:/bin"
```
The value of `$PATH` to set at the top of the crontab.

```
backup_verbosity: 0
```
The verbosity with which to run `borgmatic`. See [borgmatic command-line reference](https://torsion.org/borgmatic/docs/reference/command-line/).

```
backup_user: root
```
The user that will execute the backups and own the various backup-related files and directories.

```
backup_group: root
```
The group that will own the various backup-related files and directories.

```
backup_config_directory: /etc/borgmatic
```
The directory into which the `borgmatic` config file will be placed.

```
backup_log_file: /var/log/borgmatic.log
```
The file into which the `borgmatic` output will be logged.

### Installation-related

```
backup_borg_keyserver: hkps://keys.openpgp.org
```
The GPG keyserver from which to download the `borg` public key.

```
backup_borg_gpg_fpr: 6D5BEF9ADD2075805747B70F9F88FB52FAF7B393
```
The fingerprint of the `borg` public key. See [borg documentation - security](https://borgbackup.readthedocs.io/en/stable/support.html#security).

```
backup_borg_url: https://github.com/borgbackup/borg/releases/download
```
The URL from which to download the `borg` binary.

```
backup_borg_asset: borg-linux{{ ansible_architecture [-2:] }}
```
The name of the `borg` binary asset to download.

```
backup_borg_version: 1.1.17
```
The version of the `borg` binary to download.

```
backup_borg_path: /usr/local/bin/borg
```
The path to where the `borg` binary will be installed. Note that no attempt will be made to install `borg` if this file already exists.

```
backup_borgmatic_version: 1.5.20
```
The version of `borgmatic` to install using pip.

```
backup_borgmatic_venv: /etc/borgmatic/venv
```
The virtualenv into which pip will install `borgmatic`. It will be created if it doesn't already exist.

Dependencies
------------

None

Example Playbook
----------------

    - hosts: servers

      vars:
        backup_directories:
          - /etc/myapp
          - /var/myapp
        backup_repositories:
          - user@host1:server_backup1
          - user@host2:server_backup2
        backup_storage_options:
          encryption_passphrase: secretpassword
        backup_retention_options:
          keep_daily: 7
          keep_weekly: 4
        backup_cron_jobs:
          - schedule: "0 2 * * *"

      roles:
         - { role: newtonne.backup }

License
-------

MIT
