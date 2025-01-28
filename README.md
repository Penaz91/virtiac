VirtIAC
=======

Local "Infrastructure-as-code"-like for LibVirt

(And probably yet another unfinished project)

Status: Pre-Alpha

Example virtiac.json structure
------------------------------

```
{
    "machines": {
        "machine_name": {
            "user": "username",
            "key": "path_to_ssh_key",
            "network": "network_name",
            "forwarded_ports": [
                {
                    "host": "8000",
                    "guest": "8000"
                },
                {
                    "host": "15672",
                    "guest": "15672"
                }
            ],
        }
    }
}
```

What can it do?
----------------

Not much really:

- Check if a domain exists
- List available domains
- Start an existing domain (if a `virtiac.json` is used, it will use ssh to forward ports to the host)
- Stop an existing domain (if possible, it will kill the ssh processes used to forward the ports to the host)
- SSH to an open domain (most of the times)

What's missing?
---------------

Pretty much everything else:

- Creating a domain from a `virtiac.json` spec file
- "Undefining" a domain (deleting it)
- Editing a domain structure
- Auto-mount shared folders into guests (virtiofs)
- ... Lots more

Why not use virt-lightning?
---------------------------

Because it gets REALLY close to what I would want this kind of tool to do, but for some reason its commands are confusing and machines seem to be "temporary" and not "permanent".

Also because I want to learn something new.
