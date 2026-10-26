# CtrlOne updates

Public test installers for CtrlOne Intelligence Ai+.

## Latest explicit test update: 1.3.587

- [Download test MSI](./CtrlOne-Setup-UNSIGNED-LAB-v1.3.587.msi)
- [Download versioned test Setup EXE](./CtrlOne-Setup-UNSIGNED-LAB-v1.3.587.exe)
- [Download current test Setup EXE](./CtrlOne-Setup-UNSIGNED-LAB.exe)
- [SHA256 checksums](./SHA256SUMS.txt)

These are **unsigned lab packages for testing**. Windows may ask for approval.

This build fixes false wallpaper “Applied” confirmations from an old registry path. A fresh user-session operation must finish successfully, retain the same selected logon, and pass image-policy checks. Recognized prior deployment image policies are prepared before applying the new image. Independent restrictions and foreign wallpaper policies remain protected. The source also includes the Admin Console authentication fix; that change requires a separate server deployment. The installer retains verified Desktop MSI download and Windows Installer handoff.

All eight applicable source CI workflows passed, including the new wallpaper regression groups and six server wallpaper contracts. Package byte checks do not establish rendered desktop pixels or a completed live upgrade. Retest wallpaper deployment on the VMware PC after installing.

Check for Update reads [latest-test.json](./latest-test.json). A newer test build offers an explicit download and install action using commit-pinned MSI bytes. Windows attachment security, antivirus, SmartScreen and administrator approval remain active. The signed SYSTEM/daily customer updater is separate; this catalog does not authorize unattended unsigned customer updates.

Build source: `bfcf67aad1c59effa37cc0e8b36bc16856556a76` ([source fix](https://github.com/uquicktechnologies-spec/CtrlOne_Final/pull/113)).

## Previous manual tests

- 1.3.586: [MSI](./CtrlOne-Setup-UNSIGNED-LAB-v1.3.586.msi), [versioned Setup EXE](./CtrlOne-Setup-UNSIGNED-LAB-v1.3.586.exe), [original checksums](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/b305f3ba96459b0f5670da0e60fdd846c4627068/SHA256SUMS.txt).

- 1.3.579: [MSI](./CtrlOne-Setup-UNSIGNED-LAB-v1.3.579.msi), [original Setup EXE](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/c9e87abda71348ace19f38cf66073cc4ab7798f7/CtrlOne-Setup-UNSIGNED-LAB.exe), [original checksums](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/c9e87abda71348ace19f38cf66073cc4ab7798f7/SHA256SUMS.txt).

- 1.3.577: [MSI](./CtrlOne-Setup-UNSIGNED-LAB-v1.3.577.msi), [original Setup EXE](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/d0db9f90433d70528c952e511075b2afab5abbfd/CtrlOne-Setup-UNSIGNED-LAB.exe), [original checksums](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/d0db9f90433d70528c952e511075b2afab5abbfd/SHA256SUMS.txt).

- 1.3.576: [MSI](./CtrlOne-Setup-UNSIGNED-LAB-v1.3.576.msi), [original Setup EXE](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/dd11c47c2aad298f5663de650401b364a5491173/CtrlOne-Setup-UNSIGNED-LAB.exe), [original checksums](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/dd11c47c2aad298f5663de650401b364a5491173/SHA256SUMS.txt).

- 1.3.575: [MSI](./CtrlOne-Setup-UNSIGNED-LAB-v1.3.575.msi), [original Setup EXE](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/5c2e133a9b7dc0b6a1d437228273ede7a5fb1364/CtrlOne-Setup-UNSIGNED-LAB.exe), [original checksums](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/5c2e133a9b7dc0b6a1d437228273ede7a5fb1364/SHA256SUMS.txt).
- 1.3.574: [MSI](./CtrlOne-Setup-UNSIGNED-LAB-v1.3.574.msi), [original Setup EXE](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/6974ba318cef7c55b5e032ab17265d810bc332a9/CtrlOne-Setup-UNSIGNED-LAB.exe), [original checksums](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/6974ba318cef7c55b5e032ab17265d810bc332a9/SHA256SUMS.txt).
- 1.3.573: [MSI](./CtrlOne-Setup-UNSIGNED-LAB-v1.3.573.msi), [original Setup EXE](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/3fb475a55938f16184b81ec7b3358da33794d4c5/CtrlOne-Setup-UNSIGNED-LAB.exe), [original checksums](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/3fb475a55938f16184b81ec7b3358da33794d4c5/SHA256SUMS.txt).
- 1.3.571: [MSI](./CtrlOne-Setup-UNSIGNED-LAB-v1.3.571.msi), [original Setup EXE](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/ef12169c6ce367078c59a07b29efee884a396446/CtrlOne-Setup-UNSIGNED-LAB.exe), [original checksums](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/ef12169c6ce367078c59a07b29efee884a396446/SHA256SUMS.txt).
- 1.3.570: [MSI](./CtrlOne-Setup-UNSIGNED-LAB-v1.3.570.msi), [original Setup EXE](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/90f9d4efb25be1bed98b07fe99a78420ba0c8d3e/CtrlOne-Setup-UNSIGNED-LAB.exe), [original checksums](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/90f9d4efb25be1bed98b07fe99a78420ba0c8d3e/SHA256SUMS.txt).
- 1.3.569: [MSI](./CtrlOne-Setup-UNSIGNED-LAB-v1.3.569.msi), [original Setup EXE](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/6992d7ff567ab69c9b611d4c3214f497b9b7128a/CtrlOne-Setup-UNSIGNED-LAB.exe), [original checksums](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/6992d7ff567ab69c9b611d4c3214f497b9b7128a/SHA256SUMS.txt).
- 1.3.568: [MSI](./CtrlOne-Setup-UNSIGNED-LAB-v1.3.568.msi), [original Setup EXE](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/5a1ab8209d871ca2d3a826e73f920a840ae54150/CtrlOne-Setup-UNSIGNED-LAB.exe), [original checksums](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/5a1ab8209d871ca2d3a826e73f920a840ae54150/SHA256SUMS.txt).
