# CtrlOne updates

Public installer downloads for CtrlOne Intelligence Ai+.

## Latest manual test: 1.3.569

- [Download unsigned test MSI](./CtrlOne-Setup-UNSIGNED-LAB-v1.3.569.msi)
- [Download unsigned test Setup EXE](./CtrlOne-Setup-UNSIGNED-LAB.exe)
- [SHA256 checksums](./SHA256SUMS.txt)

These are **UNSIGNED-LAB packages for manual testing**. Downloading does not install CtrlOne. Customer automatic installation remains unavailable for these unsigned packages.

Version 1.3.569 includes the public manual-test catalog integration in Check for Update, plus bounded HTTP 502 recovery. Install this bootstrap manually once to receive the new check behavior. Header and Settings then offer the catalog's latest manual test downloads, with file sizes and published checksums. The check does not automatically install a test package or propose a downgrade.

Package versions, installer structure, source inputs and compiled contents were checked. Live VMware installation, browser download, enforcement and performance acceptance remain unverified.

Build source: `bb6e190c86734c9cdf0cdf258401fbe639e1a5e4`. Test metadata is published separately in [latest-test.json](./latest-test.json); its installer URLs pin an immutable Git commit. It does not authorize a signed production update.

## Previous manual test: 1.3.568

[MSI](./CtrlOne-Setup-UNSIGNED-LAB-v1.3.568.msi) and [original Setup EXE](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/5a1ab8209d871ca2d3a826e73f920a840ae54150/CtrlOne-Setup-UNSIGNED-LAB.exe) remain available. These older files predate the new catalog integration and HTTP 502 recovery source fix. Their [original checksums](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/5a1ab8209d871ca2d3a826e73f920a840ae54150/SHA256SUMS.txt) remain pinned to the original commit.
