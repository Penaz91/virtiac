VirtIAC
=======

Local "Infrastructure-as-code"-like for LibVirt

(And probably yet another unfinished project)

Status: Pre-Alpha

Example virtiac.json structure
------------------------------

See `src/default.json`

What can it do?
----------------

Not much really:

- Check if a domain exists
- List available domains
- Start an existing domain (if a `virtiac.json` is used, it will use ssh to forward ports to the host)
- Stop an existing domain (if possible, it will kill the ssh processes used to forward the ports to the host)
- SSH to an open domain (most of the times)
- "Undefining" a domain (deleting it)

What's half-working?
--------------------

- Creating a domain from a `virtiac.json` spec file
    - It can define a machine and (via LibGuestFS) create a disk, but it can't do provisioning or unattended install.

What's missing?
---------------

Pretty much everything else:

- Editing a domain structure
- Auto-mount shared folders into guests (virtiofs)
- ... Lots more

Why not use virt-lightning?
---------------------------

Because it gets REALLY close to what I would want this kind of tool to do, but for some reason its commands are confusing when you come from other environments like Vagrant (`vl up` builds and starts machines like Vagrant, while `vl down` destroys all machines, I would expect it to stop machines instead).

Also because I want to learn something new.
