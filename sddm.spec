%define date 20220324

Name: sddm
Summary: Lightweight display manager
Version: 0.19.0
%if %{date}
Release: 12.%{date}.1
# Packaged from git for the time being -- no download URL available
# git archive --format=tar --prefix sddm-0.19.0-$(date +%Y%m%d)/ HEAD | xz -vf > sddm-0.19.0-$(date +%Y%m%d).tar.xz
Source0: https://github.com/sddm/sddm/archive/develop/%{name}-%{version}-%{date}.tar.xz
%else
Release: 1
Source0: https://github.com/sddm/sddm/releases/download/v%{version}/%{name}-%{version}.tar.xz
%endif
URL: https://github.com/sddm
Group: Graphical desktop/KDE
License: GPLv2
Source1: sddm-x11.conf
Source2: sddm.conf
Source3: sddm.pam
Source4: sddm-autologin.pam
Source5: tmpfiles-sddm.conf
Source6: sddm.sysusers
%if %omvver >= 4050000
Patch1: sddm-0.14.0-by-default-use-plasma-wayland.patch
%else
Patch1: sddm-0.14.0-by-default-use-plasma-session.patch
%endif
Patch2: https://patch-diff.githubusercontent.com/raw/sddm/sddm/pull/1489.patch
Patch3: https://patch-diff.githubusercontent.com/raw/sddm/sddm/pull/1494.patch
#Patch4: https://patch-diff.githubusercontent.com/raw/sddm/sddm/pull/1506.patch
Patch6: https://patch-diff.githubusercontent.com/raw/sddm/sddm/pull/1526.patch
BuildRequires: cmake(ECM)
BuildRequires: pkgconfig(Qt5Core)
BuildRequires: pkgconfig(Qt5Gui)
BuildRequires: pkgconfig(Qt5DBus)
BuildRequires: pkgconfig(Qt5Quick)
BuildRequires: pkgconfig(Qt5Network)
BuildRequires: pkgconfig(Qt5Qml)
BuildRequires: pkgconfig(Qt5Test)
BuildRequires: pkgconfig(libsystemd)
BuildRequires: pam-devel
BuildRequires: qt5-linguist-tools
BuildRequires: systemd-rpm-macros
Requires(pre): systemd
%systemd_requires
# needed for QtQuick
Requires: qt5-qtdeclarative
Requires: qt5-qtimageformats
Requires: distro-release-theme
%if %omvver >= 4050000
# Wayland is default DisplayServer
Requires: weston
Requires: %{_lib}qt5-output-driver-eglfs
%else
# needed to get xcb plugin on Qt platform
Requires: %{_lib}qt5-output-driver-default
# For /etc/X11/Xsession
Requires: xinitrc
%endif
Provides: dm

%description
Lightweight display manager (login screen).

%prep
%if %{date}
%autosetup -n %{name}-%{version}-%{date} -p1
%else
%autosetup -p1
%endif

sed -i -e 's,system-login,system-auth,g' services/*.pam

%cmake_kde5 \
%if %omvver < 4050000
    -DSESSION_COMMAND:PATH=%{_datadir}/X11/xdm/Xsession \
%endif
    -DUID_MIN="1000" \
    -DUID_MAX="60000"

%build
%ninja -C build

%install
%ninja_install -C build

install -Dpm 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sddm.conf
install -Dpm 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/pam.d/sddm
install -Dpm 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/pam.d/sddm-autologin
install -Dpm 644 %{SOURCE5} %{buildroot}%{_tmpfilesdir}/sddm.conf
install -Dpm 644 %{SOURCE6} %{buildroot}%{_sysusersdir}/sddm.conf

mkdir -p %{buildroot}/run/%{name}
mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}
mkdir -p %{buildroot}%{_sysconfdir}/sddm.conf.d
# use omv-background.png as sddm background for all themes
sed -i -e 's,\(^background=\).*,\1%{_datadir}/mdk/backgrounds/OpenMandriva-splash.png,' %{buildroot}%{_datadir}/sddm/themes/elarun/theme.conf
sed -i -e 's,\(^background=\).*,\1%{_datadir}/mdk/backgrounds/OpenMandriva-splash.png,' %{buildroot}%{_datadir}/sddm/themes/maldives/theme.conf

%if %omvver < 4050000
install -Dpm 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sddm.conf.d/x11.conf
%endif

%pre
%sysusers_create_package %{name} %{SOURCE6}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%{_bindir}/%{name}
%{_bindir}/%{name}-greeter
%{_datadir}/%{name}
%dir %{_sysconfdir}/sddm.conf.d
%{_sysconfdir}/sddm.conf
%if %omvver < 4050000
%{_sysconfdir}/sddm.conf.d/x11.conf
%endif
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.DisplayManager.conf
%{_sysconfdir}/pam.d/%{name}
%{_sysconfdir}/pam.d/%{name}-greeter
%{_sysconfdir}/pam.d/%{name}-autologin
%{_sysusersdir}/sddm.conf
%{_tmpfilesdir}/sddm.conf
%{_libexecdir}/sddm-helper*
%{_unitdir}/%{name}.service
%{_libdir}/qt5/qml/SddmComponents
%attr(0711,root,sddm) %dir /run/sddm
%attr(1770,sddm,sddm) %dir %{_localstatedir}/lib/%{name}
