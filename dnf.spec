%global gitrev 4c0def8
%global hawkey_version 0.3.9
%global librepo_version 0.0.2-2.20130318gitb3c3323%{dist}

%global confdir %{_sysconfdir}/dnf

Name:		dnf
Version:	0.3.0
Release:	1.git%{gitrev}%{?dist}
Summary:	Package manager forked from Yum, using libsolv as a dependency resolver
Group:		System Environment/Base
# For a breakdown of the licensing, see PACKAGE-LICENSING
License:	GPLv2+ and GPLv2 and GPL
URL:		https://github.com/akozumpl/dnf
Source0:	http://akozumpl.fedorapeople.org/dnf-%{gitrev}.tar.xz
BuildArch:	noarch
BuildRequires:	cmake
BuildRequires:	python2
BuildRequires:	python-hawkey = %{hawkey_version}
BuildRequires:  python-iniparse
BuildRequires:	python-librepo = %{librepo_version}
BuildRequires:  python-nose
BuildRequires:  python-sphinx
BuildRequires:  rpm-python
BuildRequires:  urlgrabber
Requires:	crontabs
Requires:	libreport-filesystem
Requires:	python-hawkey = %{hawkey_version}
Requires:	python-iniparse
Requires:	python-librepo = %{librepo_version}
Requires:	rpm-python
Requires:	urlgrabber

%description
Package manager forked from Yum, using libsolv as a dependency resolver.

%prep
%setup -q -n dnf

%build
%cmake .
make %{?_smp_mflags}
make doc-man

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%check
make ARGS="-V" test

%files
%doc AUTHORS README.md COPYING PACKAGE-LICENSING
%{_bindir}/dnf
%{python_sitelib}/dnf/
%dir %{confdir}
%config(noreplace) %{confdir}/dnf.conf
%{_sysconfdir}/cron.hourly/dnf-makecache.cron
%{_sysconfdir}/libreport/events.d/collect_dnf.conf
%{_mandir}/man8/dnf.8.gz

%changelog
* Wed Mar 20 2013 Aleš Kozumplík <ales@redhat.com> - 0.3.0-1.git4c0def8
- create the cache dir ourselves. (Ales Kozumplik)
- have a user_agent const. (Ales Kozumplik)
- update readme with librepo link, tidy up. (Ales Kozumplik)
- librepo: add interface for inspecting metadata in more detail. (Ales Kozumplik)
- librepo: use a context manager for the temp dir. (Ales Kozumplik)
- librepo: support --cacheonly again. (Ales Kozumplik)
- librepo: add repo.dump() and test it using ConfigParser and StringIO. (Ales Kozumplik)
- Make --nogpgcheck work as expected again. (Ales Kozumplik)
- fix installation of gpg keys for RPM package verification. (Ales Kozumplik)
- librepo: the latest librepo version has somewhat nicer python bindings. (Ales Kozumplik)
- librepo: do not clear the packages/ when syncing new MD. (Ales Kozumplik)
- tests: add testing of Repo.get_package(). (Ales Kozumplik)
- tests: move rpms and the yum repo to the same folder. (Ales Kozumplik)
- librepo: refactor dnf.repo.Repo. (Ales Kozumplik)
- tests: bring dnf.repo.Repo under unit test. (Ales Kozumplik)
- librepo: force expiring metadata, making 'dnf makecache' work again. (Ales Kozumplik)
- librepo: downloading packages works again. (Ales Kozumplik)
- fix bug in LibrepoCallbackAdaptor causing the progreess bar go nuts on 2nd repo. (Ales Kozumplik)
- repo.gpgcheck does not mean repo.repo_gpgcheck. (Ales Kozumplik)
- repo: better error reporting in sync() (Ales Kozumplik)
- tests: make test_configure_repos() pass again. (Ales Kozumplik)
- delete YumTextMeter. (Ales Kozumplik)
- librepo: make the text progress bar work again. (Ales Kozumplik)
- Finally: download repos through librepo. (Ales Kozumplik)
- Cli._configure_repos() uses get_multiple(). (Ales Kozumplik)
- base.repos is now a dict itself. (Ales Kozumplik)
- dnf.repo.Repo: add dummy callback setters. (Ales Kozumplik)
- tests: RepoDict allows simplifying MockYumBase. (Ales Kozumplik)
- librepo: use the new Repo and RepoDict. (Ales Kozumplik)
- add dnf.util.empty(). (Ales Kozumplik)
- remove: base.add_enable_repo. (Ales Kozumplik)
- move yum.Base to yum.base.Base. (Ales Kozumplik)
- strip things out of dnf/yum/__init__.py (Ales Kozumplik)
- remove: _YumCostExclude, unused. (Ales Kozumplik)
- removing: trim down dnf.yum.packages. (Ales Kozumplik)
- removal: pruning imports in dnf.yum.__init__ (Ales Kozumplik)
- Repo and RepoDict. (Ales Kozumplik)
- tests: suite hawkey change 54f4f0f introducing make_cache_dir Sack() parameter. (Ales Kozumplik)
- doc: document clean_requirements_on_remove is on by default. (Ales Kozumplik)
- remove yum references from the default dnf.conf (RhBug:919714) (Ales Kozumplik)
- New build: 0.2.22-1 (Ales Kozumplik)
- New version: dnf-0.2.22 (Ales Kozumplik)
- move is_glob_pattern() to dnf.util (Ales Kozumplik)
- validate parameter never used in Base.read_repos() (Ales Kozumplik)
- cosmetic: refactor: getReposFromConf*() -> read_*_repos() (Ales Kozumplik)
- refactor: introduce Cli.command property. (Ales Kozumplik)
- repos: get rid of Base.prerepoconf. (Ales Kozumplik)
- repos: simplify how repos are set up. (Ales Kozumplik)
- always use iniparse, do not fallback to ConfigParser. (Ales Kozumplik)
- 'dnf repolist' is silent. (Ales Kozumplik)
- enabling/disabling repos doesn't respect the cmdline order. (RhBug:913143) (Ales Kozumplik)
- install by filenames and globbed filenames (RhBug:912130) (Ales Kozumplik)
- doc: man page: better describe the input patterns. (Ales Kozumplik)
- tests: test_installroot_with_etc() broken on other machines. (Ales Kozumplik)
- fix globbing installs again. (Ales Kozumplik)
- 'dnf list' shouldn't look for provides. (Ales Kozumplik)
- pass installroot to the sack. (RhBug:RhBug) (Ales Kozumplik)
- fix traceback in Cli.configure() with --installroot (Ales Kozumplik)
- at least do not traceback if history undo doesn't work. (Ales Kozumplik)
- adapt to new interface hawkey.Subject interface (34bae0c) (Ales Kozumplik)
- search: try to make the better matches come on top. (Ales Kozumplik)
- search: perform the search case-insensitive. (Ales Kozumplik)
- tests: bring the cli.search() method under the test. (Ales Kozumplik)
- repo: when reverting repomd.xml make sure we reset its srcfile (RhBug:904706) (Ales Kozumplik)

* Fri Mar 1 2013 Aleš Kozumplík <ales@redhat.com> - 0.2.22-1.git97180b8
- move is_glob_pattern() to dnf.util (Ales Kozumplik)
- validate parameter never used in Base.read_repos() (Ales Kozumplik)
- cosmetic: refactor: getReposFromConf*() -> read_*_repos() (Ales Kozumplik)
- refactor: introduce Cli.command property. (Ales Kozumplik)
- repos: get rid of Base.prerepoconf. (Ales Kozumplik)
- repos: simplify how repos are set up. (Ales Kozumplik)
- always use iniparse, do not fallback to ConfigParser. (Ales Kozumplik)
- 'dnf repolist' is silent. (Ales Kozumplik)
- enabling/disabling repos doesn't respect the cmdline order. (RhBug:913143) (Ales Kozumplik)
- install by filenames and globbed filenames (RhBug:912130) (Ales Kozumplik)
- doc: man page: better describe the input patterns. (Ales Kozumplik)
- tests: test_installroot_with_etc() broken on other machines. (Ales Kozumplik)
- fix globbing installs again. (Ales Kozumplik)
- 'dnf list' shouldn't look for provides. (Ales Kozumplik)
- pass installroot to the sack. (RhBug:915048) (Ales Kozumplik)
- fix traceback in Cli.configure() with --installroot (Ales Kozumplik)
- at least do not traceback if history undo doesn't work. (Ales Kozumplik)
- adapt to new interface hawkey.Subject interface (34bae0c) (Ales Kozumplik)
- search: try to make the better matches come on top. (Ales Kozumplik)
- search: perform the search case-insensitive. (Ales Kozumplik)
- tests: bring the cli.search() method under the test. (Ales Kozumplik)
- repo: when reverting repomd.xml make sure we reset its srcfile (RhBug:904706) (Ales Kozumplik)

* Mon Feb 11 2013 Aleš Kozumplík <ales@redhat.com> - 0.2.21-1.git050524e
- Selector.get_best_selector() should be able to handle simple version (not just EVR). (Ales Kozumplik)
- remove YumUtilBase(). (Ales Kozumplik)
- Do not check for unfinished transactions in Base.buildTransaction() (RhBug:902810) (Ales Kozumplik)
- list command accepts NEVRA combinations as arguments. (RhBug:901833) (Ales Kozumplik)
- tests: fix Cli.configure() test to pass without the main system conffile present. (Ales Kozumplik)
- tests: test toplevel from test_sanity. (Ales Kozumplik)
- case-insensitive matching in Subject. (Ales Kozumplik)

* Wed Jan 30 2013 Aleš Kozumplík <ales@redhat.com> - 0.2.20-2.gite7d9c11
- cosmetic: trailing whitespace in dnf.yum.callbacks (Ales Kozumplik)
- rename 'YumBase' to 'Base'. (Ales Kozumplik)
- remove base.yumvar property. (Ales Kozumplik)
- Get rid of preconf. (Ales Kozumplik)
- BaseConfig.overrides() (Ales Kozumplik)
- YumOptionParser._non_nones2dict() (Ales Kozumplik)
- cosmetic: trailing whitespace in dnf.yum.parser (Ales Kozumplik)
- Make the Base object accessible from the toplevel 'dnf' module. (Ales Kozumplik)
- Config option for the default userinput answer. (Ales Kozumplik)
- tests: reflect changes to querying updates in hawkey commit 961ca40. (Ales Kozumplik)

* Fri Jan 18 2013 Aleš Kozumplík <ales@redhat.com> - 0.2.20-1.gitdec970f
- fix '--exclude' command-line option (related RhBug:871892)
- Introduce --best switch to force trying latest packages in transactions ( RhBug:882211)
- fix '--disablerepo' (related RhBug:871892)
- Tell RPM it's OK to downgrade during dist-sync (RhBug:894339)
- 'dnf install' should skip already installed packages and say so. (RhBug:882851)

* Thu Jan 3 2013 Aleš Kozumplík <ales@redhat.com> - 0.2.19-1.gitb901926
- options parsing: do not access repositories before cache_c is ready. (RhBug:889706)
- move to the latest hawkey using libsolv-0.2.3

* Mon Dec 17 2012 Aleš Kozumplík <ales@redhat.com> - 0.2.18-1.git3701ad6
- Allow specifying removal with 'name.arch' and others (RhBug:877449)
- install: use Subject class to allow installation by provides (RhBug:880303)
- Remove rpmdb_warn_checks() and friends. (RhBug:884623)
- DNF should not allow .src.rpm installation (RhBug:884603).
- Some DNF commands require different Goal/Solver configuration. (RhBug:873079)
- Match ordinary package provides in 'dnf provides <provide>', not just files. (RhBug:871892)
- doc: update how arguments to commands can be specified.

* Mon Nov 26 2012 Aleš Kozumplík <ales@redhat.com> - 0.2.17-1.git6a055e6
- fix UnicodeDecodeError crash in history.py. (RhBug:877332)
- Support the 'dnf upgrade-to' command.
- fix: transaction traceback when rpmdb contains a package with no HDRID (RhBug:878823)
- Enable 'dnf distro-sync'.

* Thu Nov 15 2012 Aleš Kozumplík <ales@redhat.com> - 0.2.16-1.git9f050eb
- massive dead code removals accross the code base (3k LOC dropped)
- fix match_counter.sorted() tracebacks if its empty. (RhBug:873875)
- fix: callback error in some rpm transactions because of nonexistent Package.verEQ.
- Plain 'dnf update' ignores packages with broken deps. (RhBug:872948)
- support 'dnf upgrade' syntax to do the same thing as 'dnf update'.
- refactor: YumCommand is just Command now.
- Split Cli out of the YumBaseCli eintopf.
- Enable 'dnf reinstall <pkg> again.

* Thu Nov 8 2012 Aleš Kozumplík <ales@redhat.com> - 0.2.15-3.git5d85f6b
- support full NEVRA specification for the erase and install commands. (RhBug: 867553)
- Enable check-update command. (RhBug: 868810)
- Support listing patterned obsoletes.
- fix traceback: list --showduplicates.

* Wed Oct 17 2012 Aleš Kozumplík <ales@redhat.com> - 0.2.14-2.git4831982
- works against hawkey-0.3.0
- search: sort so same matched keywords stay next to each other.
- Add custom ABRT collector.
- fix: _preload_file() does the right thing when destfn does not exist.
- Make the logfiles readable by everyone.
- yumRepo: log when we are leaving MD files behind and don't know why.
- Support globs in the install command when multilib_policy is 'best'. (RhBug: 864710)
- Fix failing unit tests on i686.

* Fri Oct 5 2012 Aleš Kozumplík <ales@redhat.com> - 0.2.13-1.gitda60a96
- fix: traceback in YumBase.verifyTransaction() for local .rpms.
- Enable the 'clean' command. (RhBug: 853940)
- download no sqlite metadata.
- Reenable the search command. (RhBug: 853940)

* Fri Sep 21 2012 Aleš Kozumplík <ales@redhat.com> - 0.2.12-1.git832ecd1
- fix 'dnf --version'. (RhBug: 857710)
- Latest hawkey compatibilities.
- Run 'make check' when building the RPM.

* Thu Sep 13 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.2.11-1.git9da1268
- Make 'dnf help' work. (RhBug: 853923)
- Add the man page. (RhBug: 853923)

* Thu Aug 30 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.2.10-1.gitb06d183
- Latest hawkey compatibilities.
- RhBug: 852803

* Thu Aug 23 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.2.9-1.git5dea6e7
- Latest hawkey compatibilities.
- RhBug: 847098

* Mon Aug 6 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.2.7-6.git8ac0959
- Maintenance build to conform the new hawkey repo loading APIs.

* Tue Jul 24 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.2.7-5.git632e1eb
- Clean dependencies during 'dnf erase'.
- fixed: readline problems under pdb.
- 'dnf info' now works.
- removal: yum.sqlitesack, yum.packageSack and RPMDBPackageSack.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.7-3.gitb74addd
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.2.7-2.gitb74addd
- Add missing rpmUtils.error.

* Mon Jul 16 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.2.7-1.git3f2389e
- First Fedora rawhide build.

* Wed Jul 11 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.2.6-11.gitb1f1c08
- More licensing changes.

* Mon Jul 9 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.2.6-10.git964faae
- Licensing changes.

* Thu Jun 21 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.2.6-9.gitb4aa5c1
- More spec fixes.

* Tue Jun 19 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.2.6-8.gitb4aa5c1
- Fix rpmlint issues.

* Wed Jun 13 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.2.6-6.git9d95cc5
- Depend on the latest python-hawkey.

* Tue Jun 12 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.2.6-4.git2791093
- Fix missing cli/__init__.py

* Fri Jun 8 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.2.6-3	.git365322d
- Logging improvements.

* Wed May 16 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.2.5-2.gitf594065
- erase: remove dependants along with their dependency.

* Mon May 14 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.2.4-3.gite3adb52
- Use cron to prefetch metadata.
- Always loads filelists (attempts to fix some resolving problems).

* Mon May 7 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.2.3-1.gitbbc0801
- Fix assert in hawkey's sack.c.

* Fri May 4 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.2.2-6.git6787583
- support plain 'dnf update'.
- disable plugins.

* Thu Apr 26 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.2.1-2.gitde732f5
- Create 'etc/dnf/dnf.conf'.

* Wed Apr 25 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.2.0-2.git70753dd
- New version.

* Thu Apr 12 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.1-0.git833c054
- Initial package.
