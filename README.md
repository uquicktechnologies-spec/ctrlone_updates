# CtrlOne updates

Public test installers for CtrlOne Intelligence Ai+.

## Latest explicit test update: 1.3.571

- [Download test MSI](./CtrlOne-Setup-UNSIGNED-LAB-v1.3.571.msi)
- [Download test Setup EXE](./CtrlOne-Setup-UNSIGNED-LAB.exe)
- [SHA256 checksums](./SHA256SUMS.txt)

These are **unsigned lab packages for testing**. Install 1.3.571 once to add the new explicit update flow to older versions. Windows may ask for approval.

In 1.3.571, an equal installed version is shown as up to date. A validated newer version shows a green **Update Available** action. Clicking that action downloads and verifies the pinned MSI and opens Windows Installer in the initiating user's normal Windows session. Completing an availability check alone does not start installation. “Windows Installer opened” confirms handoff; complete the installer to finish upgrading.

CtrlOne's unsigned-package confirmation no longer blocks this explicit test action. Windows continues to apply its configured attachment security, antivirus, SmartScreen and administrator approval policies. The signed SYSTEM/daily automatic updater remains separate; this catalog does not authorize unattended unsigned customer updates. Successfully handed-off normal-user MSI sources remain available for Windows Installer.

The catalog is [latest-test.json](./latest-test.json); its installer URLs pin an immutable Git commit. The separate PC status popup remains independent of update progress.

UI, native fake-port, race, startup-order, source/type and console/database checks passed. Package versions, source inputs, installer contents and actual compiled assets were checked as files. Live VMware installation and upgrade acceptance remain unverified.

Build source: `b991d9b91a2185ac6d6347777119069303b6bf94`.

## Previous manual tests

- 1.3.570: [MSI](./CtrlOne-Setup-UNSIGNED-LAB-v1.3.570.msi), [original Setup EXE](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/90f9d4efb25be1bed98b07fe99a78420ba0c8d3e/CtrlOne-Setup-UNSIGNED-LAB.exe), [original checksums](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/90f9d4efb25be1bed98b07fe99a78420ba0c8d3e/SHA256SUMS.txt).
- 1.3.569: [MSI](./CtrlOne-Setup-UNSIGNED-LAB-v1.3.569.msi), [original Setup EXE](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/6992d7ff567ab69c9b611d4c3214f497b9b7128a/CtrlOne-Setup-UNSIGNED-LAB.exe), [original checksums](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/6992d7ff567ab69c9b611d4c3214f497b9b7128a/SHA256SUMS.txt).
- 1.3.568: [MSI](./CtrlOne-Setup-UNSIGNED-LAB-v1.3.568.msi), [original Setup EXE](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/5a1ab8209d871ca2d3a826e73f920a840ae54150/CtrlOne-Setup-UNSIGNED-LAB.exe), [original checksums](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/5a1ab8209d871ca2d3a826e73f920a840ae54150/SHA256SUMS.txt).
