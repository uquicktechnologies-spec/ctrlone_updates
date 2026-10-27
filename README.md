# CtrlOne updates

Public test installers for CtrlOne Intelligence Ai+.

## Latest explicit test update: 1.3.589

- [Download test MSI](./CtrlOne-Setup-UNSIGNED-LAB-v1.3.589.msi)
- [Download versioned test Setup EXE](./CtrlOne-Setup-UNSIGNED-LAB-v1.3.589.exe)
- [Download current test Setup EXE](./CtrlOne-Setup-UNSIGNED-LAB.exe)
- [SHA256 checksums](./SHA256SUMS.txt)

These are **unsigned lab packages for testing**. Windows may ask for approval.

This build fixes MSI reader thread affinity, bounds verification before installer authorization to 90 seconds, and reports Downloading, Verifying and Opening Windows Installer separately. Status errors, observation timeouts and dialog dismissal retain the original request. Check status reconciles that request without another installer launch. A lost start acknowledgement remains uncertain rather than permitting a blind retry.

If an installed 1.3.587 updater remains stuck at Verifying the MSI, manually install the verified 1.3.589 MSI once to replace that running updater. The fix cannot change an already running older helper. Handle normal Windows approval prompts yourself.

All nine applicable source CI workflows passed, with 19 successful jobs and one expected unrequested installer skip. Actual package/source/compiled-byte checks passed. These checks do not establish the exact cause of the photographed VMware wait or a completed live upgrade; retest after installing the corrected service.

Check for Update reads [latest-test.json](./latest-test.json). A newer test build offers an explicit download and install action using commit-pinned MSI bytes. Windows attachment security, antivirus, SmartScreen and administrator approval remain active. The signed SYSTEM/daily customer updater is separate; this catalog does not authorize unattended unsigned customer updates.

Build source: `68a56c3ca87e6c1cca7dd0dbd6e2c8e53a9797eb` ([source fix](https://github.com/uquicktechnologies-spec/CtrlOne_Final/pull/120)). Existing wallpaper display selection, upload compatibility, enrollment and file/handoff protections are retained.

## Previous manual tests

- 1.3.588: [MSI](./CtrlOne-Setup-UNSIGNED-LAB-v1.3.588.msi), [versioned Setup EXE](./CtrlOne-Setup-UNSIGNED-LAB-v1.3.588.exe), [original checksums](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/6a79ae0476a33db705a94000c1fc233cd0b05991/SHA256SUMS.txt).


- 1.3.587: [MSI](./CtrlOne-Setup-UNSIGNED-LAB-v1.3.587.msi), [versioned Setup EXE](./CtrlOne-Setup-UNSIGNED-LAB-v1.3.587.exe), [original checksums](https://raw.githubusercontent.com/uquicktechnologies-spec/ctrlone_updates/890b5fca14717e811ed8dc1c0c2fb517806e8ab3/SHA256SUMS.txt).


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
