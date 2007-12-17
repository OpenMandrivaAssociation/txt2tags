%define name txt2tags
%define version 2.3
%define release %mkrel 1

Name: %{name}
Version: %{version}
Release: %{release}
Summary: Converts text files to HTML, XHTML, sgml, LaTeX, man, etc
Group: Text tools
License: GPL
URL: http://txt2tags.sourceforge.net
# original source file is .tgz. Here it's bzipped as per Mandriva policy
Source: http://txt2tags.sourceforge.net/src/%{name}-%{version}.tar.bz2
Requires: python
BuildArch: noarch
BuildRequires: gettext

%description
Txt2tags is a generic text converter. From a simple text file with minimal
markup, it generates documents on the following formats: HTML, XHTML, sgml,
LaTeX, Lout, man, Magic Point (mgp), MoinMoin and Adobe PageMaker. Supports
heading, font beautifiers, verbatim, quote, link, lists, table and image.
There are GUI, Web and cmdline interfaces. It's a single Python script and
no external commands or libraries are needed.

%prep
%setup -q

# compile the translated messages for all languages
%define LANGS $(cd po; ls *.po | cut -d. -f1)
for lang in %{LANGS}; do
        msgfmt -o po/$lang.mo po/$lang.po
done

%install
chmod 644 extras/*

# executables
install -d %{buildroot}%{_bindir}
install -m 0755 %{name} %{buildroot}%{_bindir}

# man pages
install -d %{buildroot}/%{_mandir}/man1
install -m 0644 doc/manpage.man %{buildroot}/%{_mandir}/man1/txt2tags.1
rm doc/manpage.man

cd doc
for lang in $(ls -p1 | grep / | cut -d/ -f1); do
  if [ ! -z $(ls $lang | grep .man) ]; then
    install -d %{buildroot}/%{_mandir}/$lang/man1
    install -m 0644 $lang/$(ls $lang | grep .man) %{buildroot}/%{_mandir}/$lang/man1/txt2tags.1
    rm $lang/$(ls $lang | grep .man)
  fi
done
cd ..

# translations
for lang in %{LANGS}; do
        install -d \
                %{buildroot}%{_datadir}/locale/$lang/LC_MESSAGES
        install -m 0644 po/$lang.mo \
                %{buildroot}%{_datadir}/locale/$lang/LC_MESSAGES/txt2tags.mo
done

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,0755)
%doc ChangeLog README README-FIRST COPYING TEAM TODO
%doc %dir doc %dir extras %dir samples 
%{_bindir}/%{name}
%{_mandir}/man1/txt2tags.1*
%{_mandir}/*/man1/txt2tags.1*
%{_datadir}/locale/*/LC_MESSAGES/txt2tags.mo

