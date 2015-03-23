%define date 0

Name: sddm
Summary: Lightweight display manager
Version: 0.11.0
%if %date
Release: 0.%date.1
# Packaged from git for the time being -- no download URL available
Source0: sddm-%date.tar.xz
%else
Release: 18
Source0: https://github.com/sddm/sddm/archive/%{name}-%{version}.tar.gz
%endif
# Adds sddm to drakedm
Source1: 11sddm.conf
Source2: sddm.conf
Source3: sddm.pam
Source4: sddm-autologin.pam
Source5: tmpfiles-sddm.conf
Patch0: sddm-config.patch
Patch1:	sddm-wait-for-display-script.patch
URL: https://github.com/sddm
Group: Graphical desktop/KDE
License: GPLv2
BuildRequires: cmake
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
BuildRequires: qmake5
BuildRequires: ninja
# For /etc/X11/Xsession
Requires: xinitrc
Requires(post,preun):	rpm-helper
# needed to get xcb plugin on Qt platform
Requires:	qt5-output-driver-default
# needed for QtQuick
Requires:	qt5-qtdeclarative

%description
Lightweight display manager (login screen)

%prep
%if %date
%setup -q -n %name-%date
%else
%setup -q
%endif
%apply_patches

sed -i -e 's,system-login,system-auth,g' services/*.pam

%cmake \
	-DUSE_QT5:BOOL=ON \
	-DSESSION_COMMAND:FILEPATH=/etc/X11/Xsession \
	-DENABLE_JOURNALD=ON \
	-G Ninja

%build
ninja -C build

%install
DESTDIR="%{buildroot}" ninja install -C build

install -Dpm 644 %{SOURCE1} %{buildroot}%{_datadir}/X11/dm.d/11sddm.conf
install -Dpm 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sddm.conf
install -Dpm 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/pam.d/sddm
install -Dpm 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/pam.d/sddm-autologin
install -Dpm 644 %{SOURCE5} %{buildroot}%{_tmpfilesdir}/sddm.conf

mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}

# use default.png as sddm background
sed -i -e 's,\(^background=\).*,\1%{_datadir}/mdk/backgrounds/default.png,' %{buildroot}%{_datadir}/sddm/themes/*/theme.conf

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
%{_localstatedir}/lib/%{name}
