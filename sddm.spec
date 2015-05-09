%define date 0

Name: sddm
Summary: Lightweight display manager
Version: 0.11.0
%if %date
Release: 0.%date.1
# Packaged from git for the time being -- no download URL available
Source0: sddm-%date.tar.xz
%else
Release: 23
Source0: https://github.com/sddm/sddm/archive/%{name}-%{version}.tar.gz
%endif
# Adds sddm to drakedm
Source1: 11sddm.conf
Source2: sddm.conf
Source3: sddm.pam
Source4: sddm-autologin.pam
Source5: tmpfiles-sddm.conf
Source6: omv-background.png
Patch0: sddm-config.patch
Patch1: sddm-wait-for-display-script.patch
Patch2: sddm-0.11.0-reload-config-after-displayScript-finish.patch
Patch3: sddm-0.11.0-pass-locale-env.patch

# git patches
Patch100: 0001-Replace-signal-handling-method-of-detecting-X-startu.patch
Patch101: 0002-Don-t-set-the-DISPLAY-environment-to-the-process-tha.patch
Patch102: 0003-Don-t-pass-a-display-ID-to-X-let-X-figure-out-what-I.patch
Patch103: 0004-Fix-one-last-typo.patch
Patch104: 0005-Honour-TryExec-in-X-session-desktop-files.patch
Patch105: 0006-Allow-SYSTEMD_SYSTEM_UNIT_DIR-to-be-overidden.patch
Patch106: 0007-Add-Arabic-translation.patch
Patch107: 0008-Start-adding-next-release-highlights.patch
Patch108: 0009-ChangeLog-Remove-empty-line.patch
Patch109: 0010-Set-PAM_XDISPLAY-only-if-defined.patch
Patch110: 0011-Include-random-to-fix-FreeBSD-builds.patch
Patch111: 0012-Fix-session-startup-with-zsh.patch
Patch112: 0013-Add-Hungarian-translation.patch
Patch113: 0014-Portuguese-language-update.patch
Patch114: 0015-Update-it.ts.patch
Patch115: 0016-add-comma-separation-note-for-HideUsers.patch
Patch116: 0017-cleanup.patch
Patch117: 0018-minor-fixes-on-Turkish-translation.patch
Patch118: 0019-handle-merge-of-libsystemd-journal-libsystemd-for-sy.patch
Patch119: 0020-Allow-to-specify-QT_IMPORTS_DIR.patch
Patch120: 0021-Add-XephyrPath-option-instead-of-hardcoded-string.patch
Patch121: 0022-Improve-Russian-translation.patch
Patch122: 0023-Add-russian-translation-improvements-to-ChangeLog.patch
Patch123: 0024-should-there-be-a-problem-with-the-sddm-user-be-more.patch
Patch124: 0026-Correcting-small-typo-in-TextConstants.qml.patch
Patch125: 0028-Check-for-TryExec-in-PATH-if-it-is-not-absolute.patch

URL: https://github.com/sddm
Group: Graphical desktop/KDE
License: GPLv2
BuildRequires: cmake(ECM)
BuildRequires: pkgconfig(Qt5Core)
BuildRequires: pkgconfig(Qt5Gui)
BuildRequires: pkgconfig(Qt5Declarative)
BuildRequires: pkgconfig(Qt5DBus)
BuildRequires: pkgconfig(Qt5Quick)
BuildRequires: pkgconfig(Qt5Test)
BuildRequires: pkgconfig(systemd)
BuildRequires: pkgconfig(libsystemd-journal)
BuildRequires: pam-devel
BuildRequires: qt5-linguist-tools
# For /etc/X11/Xsession
Requires: xinitrc
Requires(post,preun):	rpm-helper
# needed to get xcb plugin on Qt platform
Requires:	qt5-output-driver-default
# needed for QtQuick
Requires:	qt5-qtdeclarative

%description
Lightweight display manager (login screen).

%prep
%if %date
%setup -q -n %name-%date
%else
%setup -q
%endif
%apply_patches

sed -i -e 's,system-login,system-auth,g' services/*.pam

%cmake_kde5 \
	-DUSE_QT5:BOOL=ON \
	-DSESSION_COMMAND:FILEPATH=/etc/X11/Xsession \
	-DENABLE_JOURNALD=ON

%build
%ninja -C build

%install
%ninja_install -C build

install -Dpm 644 %{SOURCE1} %{buildroot}%{_datadir}/X11/dm.d/11sddm.conf
install -Dpm 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sddm.conf
install -Dpm 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/pam.d/sddm
install -Dpm 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/pam.d/sddm-autologin
install -Dpm 644 %{SOURCE5} %{buildroot}%{_tmpfilesdir}/sddm.conf

mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}

# use omv-background.png as sddm background for all themes
install -Dpm 644 %{SOURCE6} %{buildroot}%{_datadir}/%{name}/themes/omv-background.png
sed -i -e 's,\(^background=\).*,\1%{_datadir}/%{name}/themes/omv-background.png,' %{buildroot}%{_datadir}/sddm/themes/*/theme.conf

%pre
%_pre_useradd sddm %{_var}/lib/sddm /bin/false

%postun
%_postun_userdel sddm

%files
%{_bindir}/%{name}
%{_bindir}/%{name}-greeter
%{_datadir}/%{name}
%config(noreplace) %{_sysconfdir}/sddm.conf
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.DisplayManager.conf
%{_sysconfdir}/pam.d/%{name}
%{_sysconfdir}/pam.d/%{name}-greeter
%{_sysconfdir}/pam.d/%{name}-autologin
%{_tmpfilesdir}/sddm.conf
%{_libexecdir}/sddm-helper
%{_unitdir}/%{name}.service
%{_libdir}/qt5/qml/SddmComponents
%{_datadir}/X11/dm.d/11sddm.conf
%attr(0755,sddm,sddm) %{_localstatedir}/lib/%{name}
