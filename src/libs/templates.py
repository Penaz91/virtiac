"""
This file is part of the VirtIAC Project.
Copyright © 2025-2025, Daniele Penazzo. All Rights Reserved.
The use of this code is governed by the MIT license attached.
See the LICENSE file for the full license.

Created on: 2025-02-06

Author: Penaz
"""
DOMAIN_TEMPLATE = """
<domain type="kvm">
<name>{name}</name>
<uuid>{uuid}</uuid>
<title>{title}</title>
{memory}
{cpu}
<os>
<type arch="x86_64" machine="pc">hvm</type>
<boot dev="hd"/>
<bootmenu enable="no"/>
</os>
<features>
<acpi/>
<apic/>
<pae/>
</features>
<clock offset='utc'>
<timer name='rtc' tickpolicy='catchup'/>
<timer name='pit' tickpolicy='delay'/>
<timer name='hpet' present='no'/>
</clock>
<on_poweroff>destroy</on_poweroff>
<on_reboot>restart</on_reboot>
<on_crash>destroy</on_crash>
<pm>
<suspend-to-mem enabled='no'/>
<suspend-to-disk enabled='no'/>
</pm>
<devices>
<emulator>/bin/qemu-system-x86_64</emulator>
{disks}
{shares}
{interface}
<controller type='usb'></controller>
<controller type='pci' model='pci-root'/>
<console type='pty'>
<target type='serial'/>
</console>
<console type='pty'>
<target type='virtio'/>
</console>
<channel type='unix'>
<target type='virtio' name='org.qemu.guest_agent.0' state='connected'/>
</channel>
<input type='mouse' bus='ps2'/>
<input type='keyboard' bus='ps2'/>
<graphics type="vnc" port="-1" autoport="yes" listen="127.0.0.1" keymap="en-us">
<listen type="address" address="127.0.0.1"/>
</graphics>
<memballoon model='virtio'></memballoon>
</devices>
</domain>
"""

MEMORY_TEMPLATE = """
<memory unit="MiB">{size}</memory>
<currentMemory unit="MiB">{size}</currentMemory>
<memoryBacking>
<access mode="{accessmode}" />
<source type="memfd" />
</memoryBacking>
"""

CPU_TEMPLATE = """
<vcpu placement="static">{vcpus}</vcpu>
<cpu mode="{mode}" check="{check}">
<model fallback="allow"/>
</cpu>
"""

DISK_TEMPLATE = """
<disk type="file" device="disk">
<driver name="qemu" type="{format}"/>
<source file="{path}"/>
<target dev="{dev}" bus="virtio"/>"
</disk>
"""

FS_TEMPLATE = """
<filesystem type="mount" accessmode="passthrough">
<driver type="{driver}"/>
<source dir="{source}"/>
<target dir="{target_name}"/>
</filesystem>
"""

INTERFACE_TEMPLATE = """
<interface type="network">
<source network="{network}" />
<model type="{type}"/>
</interface>
"""
