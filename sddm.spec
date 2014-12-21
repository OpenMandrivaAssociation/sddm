%define date 0

Name: sddm
Summary: Lightweight display manager
Version: 0.11.0
%if %date
Release: 0.%date.1
# Packaged from git for the time being -- no download URL available
Source0: sddm-%date.tar.xz
%else
Release: 1.1
Source0: https://github.com/sddm/sddm/archive/%{name}-%{version}.tar.gz
%endif
# Adds sddm to drakedm
Source1: 11sddm.conf
Source2: sddm.conf
Patch0: sddm-config.patch
URL: https://github.com/sddm
Group: Graphical desktop/KDE
License: GPLv2
BuildRequires: cmake
BuildRequires: pkgconfig(Qt5Core) pkgconfig(Qt5Gui) pkgconfig(Qt5Declarative) pkgconfig(Qt5DBus) pkgconfig(Qt5Quick)
BuildRequires: pkgconfig(Qt5Test)
BuildRequires: pkgconfig(systemd) pkgconfig(libsystemd-journal)
BuildRequires: pam-devel
BuildRequires: qt5-linguist-tools
BuildRequires: qmake5 ninja
# For /etc/X11/Xsession
Requires: xinitrc
Requires(post,preun):	rpm-helper

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

mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}

%pre
%_pre_useradd sddm %{_datadir}/%{name} /bin/false

%postun
%_postun_userdel sddm

%post
%systemd_post %{name}

%preun
%systemd_preun %{name}

%files
%{_bindir}/%{name}
%{_bindir}/%{name}-greeter
%{_datadir}/%{name}
%config(noreplace) %{_sysconfdir}/sddm.conf
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.DisplayManager.conf
%{_sysconfdir}/pam.d/%name
%{_sysconfdir}/pam.d/%name-greeter
%{_sysconfdir}/pam.d/%name-autologin
%{_libexecdir}/sddm-helper
/lib/systemd/system/%name.service
%{_libdir}/qt5/qml/SddmComponents
%{_datadir}/X11/dm.d/11sddm.conf
%{_localstatedir}/lib/%{name}
