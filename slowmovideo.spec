# sources for slowmoVideo
%global commit0 279026ad91e034e49c712e8b7a02b3e109f1af2d
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global date0 20200516

# sources for libsvflow
%global commit1 7c31a0bf9467e774442473e8b951b09fe6eb1b9f
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})

# sources for flowBuilder
%global commit2 0fbd6ea63fb43651a09418394d512b71f8eb3025
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})

Name:           slowmovideo
Version:        0.6.0
Release:        3.%{?date0}git%{?shortcommit0}%{?dist}
Summary:        Tool that uses optical flow for generating slow-motion videos

License:        GPLv3+
URL:            https://github.com/slowmoVideo
Source0:        %{url}/slowmoVideo/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz
Source1:        %{url}/libsvflow/archive/%{commit1}/libsvflow-%{shortcommit1}.tar.gz
Source2:        %{url}/v3d-flow-builder/archive/%{commit2}/v3d-flow-builder-%{shortcommit2}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake3
BuildRequires:  desktop-file-utils
BuildRequires:  make

BuildRequires:  ffmpeg-devel
BuildRequires:  freeglut-devel
BuildRequires:  glew-devel
BuildRequires:  opencv-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtscript-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libpng-devel
BuildRequires:  zlib-devel

Provides: slowmoVideo = %{version}-%{release}
Provides: bundled(libsvflow) = 1.0.0
Provides: bundled(v3d-flow-builder)

Requires: ffmpeg


%description
slowmoVideo is an OpenSource program that creates slow-motion
videos from your footage.

%prep
%autosetup -p1 -n slowmoVideo-%{commit0}
%autosetup -T -D -a 1 -p1 -n slowmoVideo-%{commit0}
%autosetup -T -D -a 2 -p1 -n slowmoVideo-%{commit0}
rmdir src/lib/libsvflow v3d-flow-builder-%{commit2}/src/lib/libsvflow
cp -pr libsvflow-%{commit1} src/lib/libsvflow
ln -s ../../../src/lib/libsvflow v3d-flow-builder-%{commit2}/src/lib/libsvflow

# Fix headers path
sed -i -e 's|src/flowField_sV.h|include/flowField_sV.h|' v3d-flow-builder-%{commit2}/CMakeLists.txt
sed -i -e 's|src/flowRW_sV.h|include/flowRW_sV.h|' v3d-flow-builder-%{commit2}/CMakeLists.txt
sed -i -e 's|flowField_sV.h|../include/flowField_sV.h|' v3d-flow-builder-%{commit2}/src/flowBuilder.cpp
sed -i -e 's|flowRW_sV.h|../include/flowRW_sV.h|' v3d-flow-builder-%{commit2}/src/flowBuilder.cpp


%build
pushd v3d-flow-builder-%{commit2}
%cmake \
  -DUSE_DBUS=ON \
  -DOpenGL_GL_PREFERENCE=GLVND \
  -DDISABLE_INCLUDE_SOURCE=ON \
  -DENABLE_TESTS=ON

%cmake_build
popd

%cmake \
  -DUSE_DBUS=ON \
  -DENABLE_TESTS=ON

%cmake_build


%install
pushd v3d-flow-builder-%{commit2}

%cmake_install

popd

%cmake_install

# Fix and validate desktop
sed -i -e 's|/usr/share/icons/AppIcon|slowmoUI|' \
       -e '1d' \
  %{buildroot}%{_datadir}/applications/slowmoUI.desktop

mv %{buildroot}%{_datadir}/icons/AppIcon.png \
  %{buildroot}%{_datadir}/icons/slowmoUI.png

chmod -x %{buildroot}%{_datadir}/applications/slowmoUI.desktop
desktop-file-validate \
  %{buildroot}%{_datadir}/applications/slowmoUI.desktop


%check
cd "%{__cmake_builddir}"
  %{__make} UnitTests
cd -


%files
%license LICENSE.md
%doc README.md todo.org
%{_bindir}/slowmoFlowBuilder
%{_bindir}/slowmoFlowEdit
%{_bindir}/slowmoInterpolate
%{_bindir}/slowmoRenderer
%{_bindir}/slowmoUI
%{_bindir}/slowmoVideoInfo
%{_bindir}/slowmoVisualizeFlow
%{_datadir}/applications/slowmoUI.desktop
%{_datadir}/icons/slowmoUI.png


%changelog
* Thu Feb 25 2021 Nicolas Chauvet <kwizart@gmail.com> - 0.6.0-3.20200516git279026a
- Enable slowmoFlowBuilder
- Enable UnitTests

* Mon Jan 11 2021 Nicolas Chauvet <kwizart@gmail.com> - 0.6.0-2.20200516git279026a
- Fix bundled provides

* Wed Jul 15 2020 Nicolas Chauvet <kwizart@gmail.com> - 0.6.0-1
- Initial spec file
