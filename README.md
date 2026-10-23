# CtrlOne updates

Public test installers for CtrlOne Intelligence Ai+.

## Latest explicit test update: 1.3.578

- [Download test MSI](./CtrlOne-Setup-UNSIGNED-LAB-v1.3.578.msi)
- [Download test Setup EXE](./CtrlOne-Setup-UNSIGNED-LAB.exe)
- [SHA256 checksums](./SHA256SUMS.txt)

These are **unsigned lab packages for testing**. Windows may ask for approval.

Version 1.3.578 fixes wallpaper downloads for PCs that use a stored legacy device token. Downloads retain device and server credential binding, refuse redirects, validate the image digest, and reject results if enrollment changes during the download. The server also rechecks current device access before serving the image. Installing this package does not restore retired devices or change administrator access. Live wallpaper application requires a new deployment after upgrading and has not yet been verified.

Version 1.3.577 requires current local enrollment proof before showing Enrolled, keeps an enrollment refusal visible during refresh, and confirms native persistence before committing a retry. Delayed retry writes are guarded against a changed server, PC, credential, enrollment generation or service restart. Repair requires an authenticated heartbeat for the same current registration. Administrator retirement and revocation are preserved; installing this update does not restore a retired PC automatically.

Version 1.3.576 reports registration storage failures before confirming registration and prevents a delayed license-lock update within the same agent process from replacing a newer registration. Connection repair separates authenticated heartbeat confirmation from local report queue status and discards results after the selected server, device or session changes. A locally unconfirmed enrollment immediately removes an older Online observation. Empty or unreadable V2 credentials remain unconfirmed; retired or revoked PCs still require administrator action.

Version 1.3.575 retries an identical installer-result acknowledgement without launching Windows Installer again, handles bounded Windows connection-table growth, and shows a specific Windows failure stage and error code when available. An unconfirmed handoff blocks the same retained request while its bounded in-memory record exists; this safeguard does not persist across service restart or history eviction. Affected older builds may need the direct MSI for their first upgrade because their installed helper is unchanged until the new build is installed.

Version 1.3.574 fixes legacy registration-token handling and distinguishes a local credential read or binding failure from a management server rejection. A pending registration stays unconfirmed while the console observes the agent's result. Existing V2 enrollment authority, server identity checks and administrator revocation remain in force. This update does not silently reset credentials or migrate a PC to another server.

The two management domains must not be assumed to be aliases: separate server installations require registration with the intended server. Use the server origin, such as `https://ctrlone.rossarimail.com`, in the connection settings; return to that server's Admin Console after registration succeeds.

An equal installed version is shown as up to date. A validated newer version shows a green **Update Available** action. Clicking that action downloads and verifies the pinned MSI and opens Windows Installer in the initiating user's normal Windows session. Completing an availability check alone does not start installation. “Windows Installer opened” confirms handoff; complete the installer to finish upgrading.

CtrlOne's unsigned-package confirmation does not block this explicit test action. Windows continues to apply its configured attachment security, antivirus, SmartScreen and administrator approval policies. The signed SYSTEM/daily automatic updater remains separate; this catalog does not authorize unattended unsigned customer updates. Successfully handed-off normal-user MSI sources remain available for Windows Installer.

The catalog is [latest-test.json](./latest-test.json); its installer URLs pin an immutable Git commit. The separate PC status popup remains independent of update progress.

Source regression tests and applicable source checks passed. Live connection, authentication, installation, upgrade and sustained performance acceptance remain unverified.

Build source: `a273fef8c35363d14e71fdf7959a73197bbfd938`.

## Previous manual tests

- 1.3.577: [MSI](./CtrlOne-Setup-UNSIGNED-LAB-v1.3.577.msi), [original Setup EXE](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/d0db9f90433d70528c952e511075b2afab5abbfd/CtrlOne-Setup-UNSIGNED-LAB.exe), [original checksums](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/d0db9f90433d70528c952e511075b2afab5abbfd/SHA256SUMS.txt).

- 1.3.576: [MSI](./CtrlOne-Setup-UNSIGNED-LAB-v1.3.576.msi), [original Setup EXE](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/dd11c47c2aad298f5663de650401b364a5491173/CtrlOne-Setup-UNSIGNED-LAB.exe), [original checksums](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/dd11c47c2aad298f5663de650401b364a5491173/SHA256SUMS.txt).

- 1.3.575: [MSI](./CtrlOne-Setup-UNSIGNED-LAB-v1.3.575.msi), [original Setup EXE](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/5c2e133a9b7dc0b6a1d437228273ede7a5fb1364/CtrlOne-Setup-UNSIGNED-LAB.exe), [original checksums](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/5c2e133a9b7dc0b6a1d437228273ede7a5fb1364/SHA256SUMS.txt).
- 1.3.574: [MSI](./CtrlOne-Setup-UNSIGNED-LAB-v1.3.574.msi), [original Setup EXE](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/6974ba318cef7c55b5e032ab17265d810bc332a9/CtrlOne-Setup-UNSIGNED-LAB.exe), [original checksums](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/6974ba318cef7c55b5e032ab17265d810bc332a9/SHA256SUMS.txt).
- 1.3.573: [MSI](./CtrlOne-Setup-UNSIGNED-LAB-v1.3.573.msi), [original Setup EXE](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/3fb475a55938f16184b81ec7b3358da33794d4c5/CtrlOne-Setup-UNSIGNED-LAB.exe), [original checksums](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/3fb475a55938f16184b81ec7b3358da33794d4c5/SHA256SUMS.txt).
- 1.3.571: [MSI](./CtrlOne-Setup-UNSIGNED-LAB-v1.3.571.msi), [original Setup EXE](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/ef12169c6ce367078c59a07b29efee884a396446/CtrlOne-Setup-UNSIGNED-LAB.exe), [original checksums](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/ef12169c6ce367078c59a07b29efee884a396446/SHA256SUMS.txt).
- 1.3.570: [MSI](./CtrlOne-Setup-UNSIGNED-LAB-v1.3.570.msi), [original Setup EXE](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/90f9d4efb25be1bed98b07fe99a78420ba0c8d3e/CtrlOne-Setup-UNSIGNED-LAB.exe), [original checksums](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/90f9d4efb25be1bed98b07fe99a78420ba0c8d3e/SHA256SUMS.txt).
- 1.3.569: [MSI](./CtrlOne-Setup-UNSIGNED-LAB-v1.3.569.msi), [original Setup EXE](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/6992d7ff567ab69c9b611d4c3214f497b9b7128a/CtrlOne-Setup-UNSIGNED-LAB.exe), [original checksums](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/6992d7ff567ab69c9b611d4c3214f497b9b7128a/SHA256SUMS.txt).
- 1.3.568: [MSI](./CtrlOne-Setup-UNSIGNED-LAB-v1.3.568.msi), [original Setup EXE](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/5a1ab8209d871ca2d3a826e73f920a840ae54150/CtrlOne-Setup-UNSIGNED-LAB.exe), [original checksums](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/5a1ab8209d871ca2d3a826e73f920a840ae54150/SHA256SUMS.txt).
