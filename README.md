# deterministic_zip

A tool to generate consistent zip files.

This tool was specifically built to prevent zip file changes from triggering
AWS Lambda function updates when running `terraform apply`. Before this change,
every re-build of the zipfile would result in a different zip even if its
contents had not changed.

## Requirements

This tool currently only runs on python3.7 in order to use deflate compression
level 9.

## Installation

```sh
pip install deterministic_zip
```

## Creating a deterministic_zip

Run the following, and verify that your zip produces the same sha256 hash:

```sh
echo "The first file." > first
echo "The second file." > second
deterministic_zip archive.zip first second
sha256sum archive.zip
```

If you have `\n` line endings the result should be:

    3afbd7c9b42bd5539ffd5c40499d3d1825157ed83791dce8d7ff2694189d28d6

If you have `\r\n` line endings (Windows) the result should be:

    40e16270d62f15e7a192e88b1b301fa6540c86e7e897036b56be513341d376ed


## How does it work?

Great question! There are three tricks to building a deterministic zip.

1) Files must be added to the zip in the same order. Directory iteration order
   may vary across machines, resulting in different zips. `deterministic_zip`
   sorts all files before adding them to the zip archive.

2) Files in the zip must have consistent timestamps. If I share a directory to
   another machine, the timestamps of individual files may differ, depsite
   identical content. To achieve timestamp consistency, `deterministic_zip`
   sets the timestamp of all added files to `2019-01-01 00:00:00`. Please note
   that this __does not__ affect the timestamp of the source files.

3) Files in the zip must have consistent permissions. File permissions look
   like `-rw-r--r--` for a file that is readable by all users, and only
   writable by the user who owns the file. Similarly executable files might
   have permissions that look like: `-rwxr-xr-x` or
   `-rwx------`. `deterministic_zip` sets the permission of all files to either
   `-r--r--r--`, or `-r-xr-xr-x`. The latter is only used of the user running
   `deterministic_zip` has execute access on the file.