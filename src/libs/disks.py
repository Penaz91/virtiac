"""
This file is part of the VirtIAC Project.
Copyright © 2025-2025, Daniele Penazzo. All Rights Reserved.
The use of this code is governed by the MIT license attached.
See the LICENSE file for the full license.

Created on: 2025-02-06

Author: Penaz
"""
import logging

import guestfs

LOGGER = logging.getLogger(__name__)


def create_disk(disk):
    """
    Creates a disk
    """
    gfs_inst = guestfs.GuestFS(python_return_dict=True)
    dsk_size = disk["size"]
    dsk_format = disk["format"]
    dsk_path = disk["path"]
    LOGGER.debug(
        "Creating a %sGiB %s disk in %s",
        dsk_size,
        dsk_format,
        dsk_path
    )
    gfs_inst.disk_create(
        dsk_path, dsk_format, dsk_size * 1024 * 1024 * 1024,
        preallocation="sparse"
    )
    gfs_inst.add_drive_opts(dsk_path, format=dsk_format, readonly=0)
    gfs_inst.launch()
    devices = gfs_inst.list_devices()
    assert len(devices) == 1
    LOGGER.debug("Partitioning disk")
    gfs_inst.part_disk(devices[0], "mbr")
    partitions = gfs_inst.list_partitions()
    assert len(partitions) == 1
    gfs_inst.mkfs("ext4", partitions[0])
    gfs_inst.shutdown()
    gfs_inst.close()
