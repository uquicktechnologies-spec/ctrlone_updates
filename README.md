# CtrlOne updates

Public test installers for CtrlOne Intelligence Ai+.

## Latest explicit test update: 1.3.573

- [Download test MSI](./CtrlOne-Setup-UNSIGNED-LAB-v1.3.573.msi)
- [Download test Setup EXE](./CtrlOne-Setup-UNSIGNED-LAB.exe)
- [SHA256 checksums](./SHA256SUMS.txt)

These are **unsigned lab packages for testing**. Windows may ask for approval.

Version 1.3.573 separates connection form drafts from the active management server and confirms the native agent's configuration before changing the console route. After an explicit local connection, it verifies this physical PC's protected primary enrollment before replacing an old selected device key. Online, LAN and Both modes use the native primary-server contract. A cloud operator's selected device is retained. Failed registration or missing server check-in evidence remains unconfirmed.

The two management domains must not be assumed to be aliases: separate server installations require registration with the intended server. Use the server origin, such as `https://ctrlone.rossarimail.com`, in the connection settings; return to that server's Admin Console after registration succeeds.

An equal installed version is shown as up to date. A validated newer version shows a green **Update Available** action. Clicking that action downloads and verifies the pinned MSI and opens Windows Installer in the initiating user's normal Windows session. Completing an availability check alone does not start installation. “Windows Installer opened” confirms handoff; complete the installer to finish upgrading.

CtrlOne's unsigned-package confirmation does not block this explicit test action. Windows continues to apply its configured attachment security, antivirus, SmartScreen and administrator approval policies. The signed SYSTEM/daily automatic updater remains separate; this catalog does not authorize unattended unsigned customer updates. Successfully handed-off normal-user MSI sources remain available for Windows Installer.

The catalog is [latest-test.json](./latest-test.json); its installer URLs pin an immutable Git commit. The separate PC status popup remains independent of update progress.

The current connection-selection suite passed 420 tests and Agent Console type checks. Source-scoped GitHub checks passed. Package versions, source inputs, installer contents and actual compiled assets were checked as files. Live VMware connection, installation and upgrade acceptance remain unverified.

Build source: `ba8e7aae1fe49c08d61cd193a50daf7002a34334`.

## Previous manual tests

- 1.3.571: [MSI](./CtrlOne-Setup-UNSIGNED-LAB-v1.3.571.msi), [original Setup EXE](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/ef12169c6ce367078c59a07b29efee884a396446/CtrlOne-Setup-UNSIGNED-LAB.exe), [original checksums](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/ef12169c6ce367078c59a07b29efee884a396446/SHA256SUMS.txt).
- 1.3.570: [MSI](./CtrlOne-Setup-UNSIGNED-LAB-v1.3.570.msi), [original Setup EXE](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/90f9d4efb25be1bed98b07fe99a78420ba0c8d3e/CtrlOne-Setup-UNSIGNED-LAB.exe), [original checksums](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/90f9d4efb25be1bed98b07fe99a78420ba0c8d3e/SHA256SUMS.txt).
- 1.3.569: [MSI](./CtrlOne-Setup-UNSIGNED-LAB-v1.3.569.msi), [original Setup EXE](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/6992d7ff567ab69c9b611d4c3214f497b9b7128a/CtrlOne-Setup-UNSIGNED-LAB.exe), [original checksums](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/6992d7ff567ab69c9b611d4c3214f497b9b7128a/SHA256SUMS.txt).
- 1.3.568: [MSI](./CtrlOne-Setup-UNSIGNED-LAB-v1.3.568.msi), [original Setup EXE](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/5a1ab8209d871ca2d3a826e73f920a840ae54150/CtrlOne-Setup-UNSIGNED-LAB.exe), [original checksums](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/5a1ab8209d871ca2d3a826e73f920a840ae54150/SHA256SUMS.txt).
