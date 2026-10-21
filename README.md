# CtrlOne updates

Public installer downloads for CtrlOne Intelligence Ai+.

## Latest manual test: 1.3.570

- [Download unsigned test MSI](./CtrlOne-Setup-UNSIGNED-LAB-v1.3.570.msi)
- [Download unsigned test Setup EXE](./CtrlOne-Setup-UNSIGNED-LAB.exe)
- [SHA256 checksums](./SHA256SUMS.txt)

These are **UNSIGNED-LAB packages for manual testing**. Downloading does not install CtrlOne. Customer automatic installation remains unavailable for unsigned packages.

Version 1.3.570 separates the Header's Check for Update dialog from the PC status popup. Update checks show their own progress, results, download options and retry action. PC status shows connection diagnostics. Completing a slow update check does not reopen a dismissed update dialog over PC status.

The public manual-test catalog integration and bounded HTTP 502 recovery from 1.3.569 are included. Install this version manually; later explicit checks read [latest-test.json](./latest-test.json). Its installer URLs pin an immutable Git commit. This catalog does not authorize a signed production update.

The popup fix passed interaction tests and type checks. Package versions, installer structure, source inputs and compiled contents were checked. Live VMware installation, popup behavior, browser download, enforcement and performance acceptance remain unverified.

Build source: `e365d6d02e587f4108b68b11d746f77d71457e8a`.

## Previous manual tests

- 1.3.569: [MSI](./CtrlOne-Setup-UNSIGNED-LAB-v1.3.569.msi), [original Setup EXE](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/6992d7ff567ab69c9b611d4c3214f497b9b7128a/CtrlOne-Setup-UNSIGNED-LAB.exe), [original checksums](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/6992d7ff567ab69c9b611d4c3214f497b9b7128a/SHA256SUMS.txt).
- 1.3.568: [MSI](./CtrlOne-Setup-UNSIGNED-LAB-v1.3.568.msi), [original Setup EXE](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/5a1ab8209d871ca2d3a826e73f920a840ae54150/CtrlOne-Setup-UNSIGNED-LAB.exe), [original checksums](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/5a1ab8209d871ca2d3a826e73f920a840ae54150/SHA256SUMS.txt).
