%global gitrev 2c0cf93
%global hawkey_version 0.4.9
%global librepo_version 1.4.0
%global libcomps_version 0.1.4

%global confdir %{_sysconfdir}/dnf

Name:		dnf
Version:	0.4.14
Release:	1%{?dist}
Summary:	Package manager forked from Yum, using libsolv as a dependency resolver
Group:		System Environment/Base
# For a breakdown of the licensing, see PACKAGE-LICENSING
License:	GPLv2+ and GPLv2 and GPL
URL:		https://github.com/akozumpl/dnf
Source0:	http://akozumpl.fedorapeople.org/dnf-%{gitrev}.tar.xz
BuildArch:	noarch
BuildRequires:	cmake
BuildRequires:	python2
BuildRequires:	python-bugzilla
BuildRequires:	python-hawkey >= %{hawkey_version}
BuildRequires:	python-iniparse
BuildRequires:	python-libcomps >= %{libcomps_version}
BuildRequires:	python-librepo >= %{librepo_version}
BuildRequires:  python-nose
BuildRequires:  python-sphinx
BuildRequires:  rpm-python
BuildRequires:  systemd
Requires:	deltarpm
Requires:	libreport-filesystem
Requires:	python-hawkey >= %{hawkey_version}
Requires:	python-iniparse
Requires:	python-libcomps >= %{libcomps_version}
Requires:	python-librepo >= %{librepo_version}
Requires:	rpm-python
Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd

%description
Package manager forked from Yum, using libsolv as a dependency resolver.

%package -n python3-dnf
Summary:	Package manager forked from Yum, using libsolv as a dependency resolver
Group:		System Environment/Base
BuildRequires:	python3
BuildRequires:	python3-devel
BuildRequires:	python3-hawkey >= %{hawkey_version}
BuildRequires:	python3-iniparse
BuildRequires:	python3-libcomps >= %{libcomps_version}
BuildRequires:	python3-librepo >= %{librepo_version}
BuildRequires:	python3-nose
BuildRequires:	rpm-python3
Requires:	python3-hawkey >= %{hawkey_version}
Requires:	python3-iniparse
Requires:	python3-libcomps >= %{libcomps_version}
Requires:	python3-librepo >= %{librepo_version}
Requires:	rpm-python3

%description -n python3-dnf
Package manager forked from Yum, using libsolv as a dependency resolver.

%prep
%setup -q -n dnf
rm -rf py3
mkdir ../py3
cp -a . ../py3/
mv ../py3 ./

%build
%cmake .
make %{?_smp_mflags}
make doc-man
pushd py3
%cmake -DPYTHON_DESIRED:str=3 -DWITH_MAN=0 .
make %{?_smp_mflags}
popd

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
pushd py3
make install DESTDIR=$RPM_BUILD_ROOT
popd

%global py2pluginpath %{python_sitelib}/dnf-plugins
%global py3pluginpath %{python3_sitelib}/dnf-plugins
mkdir -p $RPM_BUILD_ROOT%{py2pluginpath}
mkdir -p $RPM_BUILD_ROOT%{py3pluginpath}

%check
make ARGS="-V" test
pushd py3
make ARGS="-V" test
popd

%files
%doc AUTHORS README.rst COPYING PACKAGE-LICENSING
%{_bindir}/dnf
%dir %{confdir}
%config(noreplace) %{confdir}/dnf.conf
%config %{_sysconfdir}/bash_completion.d/dnf-completion.bash
%{_sysconfdir}/libreport/events.d/collect_dnf.conf
%{_mandir}/man8/dnf.8.gz
%{_mandir}/man8/dnf.conf.8.gz
%{_unitdir}/dnf-makecache.service
%{_unitdir}/dnf-makecache.timer
%{python_sitelib}/dnf/
%{py2pluginpath}

%files -n python3-dnf
%doc AUTHORS README.rst COPYING PACKAGE-LICENSING
%{_bindir}/dnf
%dir %{confdir}
%config(noreplace) %{confdir}/dnf.conf
%{_sysconfdir}/libreport/events.d/collect_dnf.conf
%{_mandir}/man8/dnf.8.gz
%{_mandir}/man8/dnf.conf.8.gz
%{_unitdir}/dnf-makecache.service
%{_unitdir}/dnf-makecache.timer
%{python3_sitelib}/dnf/
%{py3pluginpath}

%post
%systemd_post dnf-makecache.timer

%preun
%systemd_preun dnf-makecache.timer

%postun
%systemd_postun_with_restart dnf-makecache.timer

%changelog

* Thu Feb 13 2014 Aleš Kozumplík <ales@redhat.com> - 0.4.14-1
- api: add Repo.pkgdir. (Ales Kozumplik)
- Make UnicodeStream Python 2 compatible (RhBug:1063022) (Radek Holy)
- Add missing yum arches to rpmUtils.arch; fix getBaseArch(). (Daniel Mach)
- Add rpmUtils.arch tests. (Daniel Mach)
- Set _ppc64_native_is_best = True in rpmUtils.arch. (RhBug:1062390) (Daniel Mach)
- clean: do not clean out files from local repos. (RhBug:1064148) (Ales Kozumplik)
- remove: groupUnremove(). (Ales Kozumplik)
- Fix undefined variable in group_remove(). (Ales Kozumplik)
- doc: Fix syntax of selected commands. (Radek Holy)
- Add repository-packages check-update command. (Radek Holy)
- refactor: dnf.cli.commands.CheckUpdateCommand (Radek Holy)
- Base RepoPkgsCommand.activate_sack on its sub-commands. (Radek Holy)
- Add repository-packages info command. (Radek Holy)
- Add repository-packages list command. (Radek Holy)
- refactor: InfoCommand interface (Radek Holy)
- Support filtering by repository name in doPackageLists. (Radek Holy)
- refactor: dnf.cli.cli.BaseCli.returnPkgLists (Radek Holy)
- doc: distro-sync spelling on the man page. (RhBug:1062847) (Ales Kozumplik)
- doc: update 0.4.13 release notes with the delta rpm rfe. (Ales Kozumplik)

* Thu Feb 6 2014 Aleš Kozumplík <ales@redhat.com> - 0.4.13-2
- remove: dnf.util.log_last_excpetion (Radek Holy)
- Make UnicodeStream text-based. (Radek Holy)
- Fix AttributeError raised by setup_stdout when stdout does not have attribute encoding. (Radek Holy)
- Make stdout patching Python 2 compatible. (Radek Holy)
- config: 'keepcache' off by in-code default. (Ales Kozumplik)
- doc: man: better explain the difference between 'check-update' and 'upgrade'. (Ales Kozumplik)
- doc: api: improve documentation of dnf.cli.Command.run(). (Ales Kozumplik)
- Allow installing by fully specified provides. (RhBug:1055051) (Ales Kozumplik)
- doc: api: dnf.cli.Command.aliases is a general sequence. (Ales Kozumplik)
- update AUTHORS (Ales Kozumplik)
- doc: document keep_cache option. (Kevin Kofler)
- Revert "remove: conf.keepcache option." (RhBug:1046244) (Kevin Kofler)
- add Elad to AUTHORS. (Ales Kozumplik)
- Add bash completion. (RhBug:#1030440) (Elad Alfassa)
- cosmetic: smooth out dnf.spec.in a bit. (Ales Kozumplik)
- doc: update the deltarpm section in cli_vs_yum a bit. (Ales Kozumplik)
- Installing a local pkg is okay. (RhBug#1056400) (Zdenek Pavlas)
- test_drpm: override the /bin/applydeltarpm detection. (Zdeněk Pavlas)
- drpm: fall back to rpm download on drpm errors (Zdenek Pavlas)
- drpm: display delta rebuilds as they finish (Zdenek Pavlas)
- drpm: spawn delta rebuild jobs, report failures (Zdenek Pavlas)
- get_package_target(): support the "donecb" callback (Zdenek Pavlas)
- drpm: download delta packages if possible (Zdenek Pavlas)
- drpm: add config options + docs, load updateinfo.xml (Zdenek Pavlas)
- tests: fix test for the new libsolv (also see hawkey commit 4c5aee1). (Ales Kozumplik)
- report mirror failures. (Zdenek Pavlas)
- progress display: end(size=None) should never fail (Zdenek Pavlas)
- fix typo in the 0.4.12 release notes. (Ales Kozumplik)

* Tue Jan 21 2014 Aleš Kozumplík <ales@redhat.com> - 0.4.12-1
- doc: groom the bandwidth, throttle option a bit. (Ales Kozumplik)
- repos: disable fastestmirror by default. (RhBug:1051554) (Ales Kozumplik)
- treat package reason 'unknown' in push_userinstalled() as 'user' (RhBug:1049025) (Ales Kozumplik)
- cli: --cacheonly beats expired repos. (RhBug:1048468) (Ales Kozumplik)
- util: function to log exceptions' tracebacks. (Ales Kozumplik)
- add "throttle" and "bandwidth" options (RhBug:1045737) (Zdenek Pavlas)
- update AUTHORS. (Ales Kozumplik)
- Spelling fixes. (Ville Skyttä)
- config: make sure faulty values do not propagate into the conf. (RhBug:1048488) (Ales Kozumplik)
- cli: fix another ridiculous capitalization. (Ales Kozumplik)
- doc: two new FAQs about MD synchronization. (Ales Kozumplik)

* Thu Jan 9 2014 Aleš Kozumplík <ales@redhat.com> - 0.4.11-1
- In an afterthought, why encourage clients to behave abnormally. (Ales Kozumplik)
- plugins: redo the plugin config loading, with doc. (Ales Kozumplik)
- plugins: --disableplugin works again. (Ales Kozumplik)
- cli: re-enable recognized options in --help. (Ales Kozumplik)
- cli: drop --enableplugin. (Ales Kozumplik)
- plugins: do not traceback on a broken plugin. (Ales Kozumplik)
- api: determine if particular metadata got refreshed (RhBug:1048988) (Ales Kozumplik)
- apichange: plugins: turns out the pluginpath has to depend on py2/py3. (Ales Kozumplik)
- doc: specify types of config options in conf_ref.rst. (Ales Kozumplik)
- packaging: bump the year. (Ales Kozumplik)
- doc: 'dnf provides' does not do extra filename heuristics. (RhBug:1048572) (Ales Kozumplik)
- doc: document 'remove' alias for 'erase'. (RhBug:1048716) (Ales Kozumplik)
- cli: cosmetic: help text incorrectly mentioning Yum. (RhBug:1048719) (Ales Kozumplik)
- fix: typo in CLI's search(). (RhBug:1048402) (Ales Kozumplik)
- refactor: cosmetic: imports in dnf.yum.config (Ales Kozumplik)
- doc: faq: 'dnf update' vs 'yum update'. (Ales Kozumplik)
- plugins: add basic support for reading in plugin config. (Ales Kozumplik)
- tests: use iniparse.compat instead of configparser. (Ales Kozumplik)
- doc: typo in 1f180f8. (Ales Kozumplik)
- doc: faq: explain a 'check-update' oddity. (Ales Kozumplik)

* Thu Jan 2 2014 Aleš Kozumplík <ales@redhat.com> - 0.4.10-1
- packaging: own the plugin directories. (Ales Kozumplik)
- doc: cli_vs_yum: no 'Processing dependency' lines. (RhBug:1044999) (Ales Kozumplik)
- doc: using --setopt from CLI. (RhBug:1044981) (Ales Kozumplik)
- doc: fix a semantic error in cli_vs_yum's skip_if_unavailable doc. (Ales Kozumplik)
- doc: tweak the 'proxy' documentation in conf_ref.rst (Ales Kozumplik)
- fix some uses of str() in unicode context. (RhBug#1044502) (Zdenek Pavlas)
- doc: document the "proxy" option. (Zdenek Pavlas)
- doc: clarify repo_id_invalid() slightly. (Ales Kozumplik)
- api: Extract repo ID validation to a separate function (RhBug:1018284) (Radek Holy)
- tests: test drpm lookup, test basic rpm downloading (Zdenek Pavlas)
- tests: add repository with delta rpms (Zdenek Pavlas)
- fix: gracefully handle the exception when cannot create the locks directory. (RhBug:1036147) (Ales Kozumplik)
- api: plugins: add hook for sack ready (RhBug:1038937) (Ales Kozumplik)
- Fix TypeError raised when comparing YumHistoryPackage in Python 3. (Radek Holy)
- Let history info command recognize 'last'. (Radek Holy)
- Let install command recognize '@' (RhBug:1036211) (Radek Holy)
- Fix AssertionError raised when undoing a package available in multiple repos (RhBug:1038403) (Radek Holy)
- Fix handling of errors raised when undoing transactions. (Radek Holy)
- get_package_target(): don't use yum compatibility attribute (Zdenek Pavlas)
- Show correct installed size. (RhBug#1040255) (Zdenek Pavlas)
- api: plugins: transaction() hook called after a transaction. (RhBug:967264) (Ales Kozumplik)
- remove: Command.needTs*(). Unused. (Ales Kozumplik)
- doc: api: dnf.cli. Commands and resgistering them. (Ales Kozumplik)
- remove: basecmd parameter to Command.run() (Ales Kozumplik)
- wip: the Command doc (Ales Kozumplik)
- py3: fix exception catching from 96128b8. (Ales Kozumplik)
- download_packages: propagate the librepo exception (RhBug:1035164) (Zdenek Pavlas)
- rename: YumTerm -> Term. (Ales Kozumplik)
- refactor: get rid of the return values from Command.run(). (Ales Kozumplik)
- rename: Cli._register_command() -> register_command(). (Ales Kozumplik)
- api: make Command available directly from dnf.cli. (Ales Kozumplik)
- rename: cli.command.Command.doCommand() -> run() (Ales Kozumplik)
- Log packages causing history undo failures. (Radek Holy)
- Add pkg_spec attribute to MarkingError. (Radek Holy)
- doc: api: Plugin.name. (Ales Kozumplik)

* Tue Dec 3 2013 Aleš Kozumplík <ales@redhat.com> - 0.4.9-1
- doc: api: initiali version of the plugin interface. (Ales Kozumplik)
- doc: api: logging. (Ales Kozumplik)
- doc: api: Base.reset() (Ales Kozumplik)
- remove: conf.keepcache option. (Ales Kozumplik)
- plugins: loading from the CLI. (Ales Kozumplik)
- plugins: test plugin loading (Ales Kozumplik)
- plugins: basic plugins loading and running. (Ales Kozumplik)
- cli: commands: state whether the command might try to modify rpmdb. (Ales Kozumplik)
- remove: dnf.yum.plugins and all references. (Ales Kozumplik)
- doc: update the --allowerasing comment. (Ales Kozumplik)
- doc: Document packages replacement command. (Radek Holy)
- Work around a bug in NamedTemporaryFile(). (RhBug:1036116) (Zdenek Pavlas)
- remove: dnf.yum.constants (Radek Holy)
- Add --allowerasing flag option (RhBug:963137) (Radek Holy)
- remove: dnf.yum.packages.PackageObject (Radek Holy)
- remove: dnf.yum.packages.FakeSack (Radek Holy)
- remove: dnf.yum.packages.FakeRepository (Radek Holy)
- reduce usage of dnf.yum.constants. (Ales Kozumplik)
- remove: bunch of old, unused Base() methods. (Ales Kozumplik)
- Set "history" reason to packages installed during undos. (Radek Holy)
- test_localPkg: test also remote packages (Zdenek Pavlas)
- remove: Package.localpath. (Ales Kozumplik)
- po.localPkg(): return the right localpath. (RhBug:1034607) (Zdenek Pavlas)
- cli: fix grammar of some sentences. (Ales Kozumplik)
- tests: cosmetic: order packages in .repo files by name. (Ales Kozumplik)
- Add "history userinstalled" command (RhBug:884615) (Radek Holy)
- Support printing of package names. (Radek Holy)
- Support iteration over packages installed by the user. (Radek Holy)
- tests: Make tests independent of locale settings. (Radek Holy)
- refactor: Do not give package-marking exceptions long messages. (Radek Holy)
- remove: Do not give package-marking exceptions translated messages. (Radek Holy)
- refactor: Raise/catch proper exceptions in/by package-marking methods. (Radek Holy)
- doc:  clarify 'Specifying Transaction' a bit. (Ales Kozumplik)
- doc: api: document marking packages for transactions in Base. (Ales Kozumplik)
- rename: Base.update*() -> Base.upgrade*() (Ales Kozumplik)
- fixed JSON decode error in persistor.py (RhBug:1032455) (Jan Silhan)
- doc: api: Base.read_all_repos() (Ales Kozumplik)
- remove: conf.config_file_age and repo.repo_config_age. (Ales Kozumplik)
- history: fix tests in py3. (Ales Kozumplik)
- tests: Remove unneeded test of HistoryCommand.doCheck. (Radek Holy)
- doc: Use imperative mood in documentation of the undo command. (Radek Holy)
- Enable the "history rollback" command (RhBug:991038) (Radek Holy)
- remove: force from history rollback command. (Radek Holy)
- Add history-rollback-specific transaction check error output. (Radek Holy)
- Fix AttributeError raised when BaseCli.history_rollback_transaction called. (Radek Holy)
- refactor: Move the content of HistoryCommand._hcmd_rollback to BaseCli.history_rollback_transaction. (Radek Holy)
- refactor: Rename Base.history_undo to Base.history_undo_operations. (Radek Holy)
- refactor: Move the content of HistoryCommand._hcmd_undo to BaseCli.history_undo_transaction. (Radek Holy)
- refactor: Move obsoleted packages handling within Base.history_undo. (Radek Holy)
- refactor: Rename functions in Base.history_undo. (Radek Holy)
- Return history of a transaction in the new container. (Radek Holy)
- Remove unneeded sack parameter from open_history. (Radek Holy)
- Add container of operations on packages by their NEVRAs. (Radek Holy)

* Thu Nov 21 2013 Aleš Kozumplík <ales@redhat.com> - 0.4.8-1
- doc: api: add DeprecationWarning. (Ales Kozumplik)
- remove: Base.run_with_package_names. (Ales Kozumplik)
- history: do not traceback if a regular user tries to look into the history DB. (Ales Kozumplik)
- cli: do not print the command name when concluding a history command. (Ales Kozumplik)
- refactor: StartupConf is no longer needed. (Ales Kozumplik)
- doc: api: reading configuration from filesystem. (Ales Kozumplik)
- refactor: move Base.read_conf_file to Cli. (Ales Kozumplik)
- config: do away with the two-phase parsing. (Ales Kozumplik)
- removed shelve support in persistor.py (Jan Silhan)
- removed per_arch_dict function from query.py (Jan Silhan)
- removed _construct_result function from query.py (Jan Silhan)
- removed latest_per_arch function from query.py (Jan Silhan)
- Fix output when downgrading not installed package (RhBug:1030980) (Radek Holy)
- remove: Conf.uid, Conf.progress_obj. (Ales Kozumplik)
- Handle remote URLs. (RhBug:1030297) (Zdenek Pavlas)
- runTransaction(): clean_used_packages() should run after verify_transaction() (Zdenek Pavlas)
- remove: dnf.yum.misc.re_remote_url() (Zdenek Pavlas)
- remove: Base.localPackages (Zdenek Pavlas)
- remove: Base._cleanup (Zdenek Pavlas)
- doc: api: document dnf.transaction.Transaction. (Ales Kozumplik)
- fix: installs globbing for a file without a slash at the start. (RhBug:1030998) (Ales Kozumplik)
- doc: api: document the dnf.subject.Subject API. (Ales Kozumplik)
- rename: Base.group_lists -> Base._group_lists. (Ales Kozumplik)
- groups: also display available environment groups. (RhBug:1029948) (Ales Kozumplik)
- removed PycompDict (Jan Silhan)
- doc: api: document Query. (Ales Kozumplik)
- No fastestmirror "status" message if detection didn't run. (Zdenek Pavlas)
- Add the "determining the fastest mirror" progress code. (Zdenek Pavlas)
- rename: queries.Query -> query.Query. queries.Subject -> subject.Subject. (Ales Kozumplik)
- refactor: initializing a Repo. (Ales Kozumplik)
- setup deprecation warnings. (Ales Kozumplik)
- refactor: do not rely on CliCache (dnf.conf.Cache previously) outside of Cli. (Ales Kozumplik)
- spec file now generates dnf and dnf-python3 packages (Jan Silhan)
- fixed py3 error when called next method (Jan Silhan)

* Fri Nov 8 2013 Aleš Kozumplík <ales@redhat.com> - 0.4.7-1
- doc: api: Conf.installonly_limit. (Ales Kozumplik)
- INSTALLONLYPKGS cleanup, add installonlypkg(kernel) (Zdenek Pavlas)
- doc: foundations of the API documentation. (Ales Kozumplik)
- doc: disable html_static_path. (Ales Kozumplik)
- Officially call dnf.yum.config.YumConfig just dnf.conf.Conf. (Ales Kozumplik)
- doc: delete the obsoleted API docs (Ales Kozumplik)
- refactor: Comps.*iter methods are not properties. (Ales Kozumplik)
- rename: Base.build_transaction() -> Base.resolve() (Ales Kozumplik)
- rename: Base.activate_sack() -> Base.fill_sack(). (Ales Kozumplik)
- remove: config.upgrade_requirements_on_install. (Ales Kozumplik)
- remove: config.group_package_types. (Ales Kozumplik)
- INSTALLONLYPKGS: fix a typo (Zdenek Pavlas)
- removed updates_by_name function from queries.py (Jan Silhan)
- removed downgrades_by_name function from queries.py (Jan Silhan)
- removed latest_available_per_arch function from queries.py (Jan Silhan)
- removed latest_installed_per_arch function from queries.py (Jan Silhan)
- removed by_file function from queries.py (Jan Silhan)
- removed installed_exact function from queries.py (Jan Silhan)
- removed by_repo function from queries.py (Jan Silhan)
- removed by_name function from queries.py (Jan Silhan)
- adapting for hawkey behaviour of latest filter option in Query (Jan Silhan)
- don't convert unicode to str and back. (RhBug:1025650) (Zdenek Pavlas)
- build: require librepo-1.3.0 (Ales Kozumplik)
- Subject.get_best_query() uses glob matching for versions (RhBug:1019170) (Ales Kozumplik)
- build: require more recent libcomps and librepo. (Ales Kozumplik)

* Wed Oct 30 2013 Aleš Kozumplík <ales@redhat.com> - 0.4.6-1
- doc: add documentation for the installonly options. (Ales Kozumplik)
- Add history-undo-specific transaction check error output. (Radek Holy)
- Move transaction check error output into commands. (Radek Holy)
- Enable the "history undo" command. (Radek Holy)
- Fix TypeError raised when Base.history_undo called with a nonempty transaction (RhBug:878348) (Radek Holy)
- Add iterators exhaustion testing function. (Radek Holy)
- Generalize the PackageMatcher to an ObjectMatcher. (Radek Holy)
- Support querying the last transaction ID in the history. (Radek Holy)
- refactor: Extract transaction IDs/offsets conversion to a standalone method. (Radek Holy)
- Create a YumHistory wrapper. (Radek Holy)
- Add iterables splitting function. (Radek Holy)
- Support skipping the depsolve stage. (Radek Holy)
- store the expired repos. (Ales Kozumplik)
- update the installonlies list. (Ales Kozumplik)
- installonly packages: enable enforcing the limit (RhBug:880524) (Ales Kozumplik)
- downloader: use LRO_FASTESTMIRRORCACHE (Zdenek Pavlas)
- downloader: enable failfast (Zdenek Pavlas)
- removed available_by_name function from dnf.queries (Jan Silhan)
- removed available_by_nevra function from dnf.queries (Jan Silhan)
- removed installed_by_nevra function from dnf.queries, added nevra Query method (Jan Silhan)
- removed installed_by_name function from dnf.queries (Jan Silhan)
- removed installed function from dnf.queries (Jan Silhan)
- fixed GPG key retrieval error (Jan Silhan)
- added to_ord function to pycomp.py (Jan Silhan)
- refactor: Remove unused parameter from CliTransactionDisplay.scriptout. (Radek Holy)
- Fix return of Reinstalled history state by TransactionItem.history_iterator. (Radek Holy)
- Move the _history_get_transaction to the BaseCli. (Radek Holy)
- cli: Output.history and Output.yumdb. (Ales Kozumplik)
- cli: do not register command instances, register command classes. (Ales Kozumplik)
- refactor: cli: command.getNames() is now command.aliases. (Ales Kozumplik)
- cli: do not display 'Setting up ... Process'. (Ales Kozumplik)
- fix: traceback in 'dnf group summary' (RhBug:1019957) (Ales Kozumplik)
- commands: recognize one-word group commands (e.g. 'grouplist') (RhBug:1020101) (Ales Kozumplik)
- tests: fix GroupOutputTest. (Ales Kozumplik)
- fix: traceback 'dnf -v group list Group'. (Ales Kozumplik)
- cli: add Command.canonical(). (Ales Kozumplik)
- comps: adapt to the latest libcomps that correctly throws KeyError in dict[]. (Ales Kozumplik)
- cli: cosmetic: remove two extra newlines before 'Dependencies resolved.' (Ales Kozumplik)
- remove: use of weakref.proxy. (Ales Kozumplik)
- remove extra member variable assignment in Base._goal2transaction(). (Ales Kozumplik)
- tests: rename: FakeTerm->MockTerminal. (Ales Kozumplik)
- tests: fixed broken test_installPkgs_notfound(). (Ales Kozumplik)
- refactor: split Output and Base objects in CLI. (Ales Kozumplik)
- full Python 3 support added (Jan Silhan)
- expired repos are saved in json instead of shelve (Jan Silhan)
- fixed shadowing of variable (Jan Silhan)
- removed needless flush from output.py (Jan Silhan)
- repo.metalink_data is gone (RhBug:1020934) (Zdenek Pavlas)
- tests: rename MockYumBase to MockBase. (Ales Kozumplik)
- refactor: Base.build_transaction() so we can unit test its core. (Ales Kozumplik)
- tests: test some obsoletes. (Ales Kozumplik)
- doc: missing newline breaking format. (Ales Kozumplik)

* Sun Oct 20 2013 Aleš Kozumplík <ales@redhat.com> - 0.4.5-1
- Fix tracebacks during downloads of obsoleting transactions. (RhBug:1021087) (Ales Kozumplik)
- fix: missing config file shouldn't cause a LibrepoExeption-triggered traceback. (Ales Kozumplik)
- py3: don't want float results here (Zdenek Pavlas)
- remove: repo.urlgrabber_opts() (Zdenek Pavlas)
- Add repo.get_handle() returning a cached librepo handle (Zdenek Pavlas)
- enhancement: LRO_FASTESTMIRROR (Zdenek Pavlas)
- enhancement: use proxy settings (Zdenek Pavlas)
- refactor: _handle_new_remote(), _handle_new_pkg_download() (Zdenek Pavlas)
- Don't confuse users when file already exists (Zdenek Pavlas)
- rename: YumBaseCli -> BaseCli. (Ales Kozumplik)
- remove: Output.printtime and Output.simpleProgressBar. (Ales Kozumplik)
- refactor: call YumOutput just Output. (Ales Kozumplik)
- refactor: move dnf.yum.base.Base to dnf.base.Base (Ales Kozumplik)

* Mon Oct 14 2013 Aleš Kozumplík <ales@redhat.com> - 0.4.4-1
- fix: missing config file shouldn't cause a LibrepoExeption-triggered traceback. (Ales Kozumplik)
- basic python 3 support added. (Jan Silhan)
- input function in dnf.i18n renamed to ucd_input to avoid conflicts with buildin function (Jan Silhan)
- Improve error reporting in hdrFromPackage() (Ales Kozumplik)
- Resetting base.goal. (Ales Kozumplik)
- fix: install does not report file conflicts (RhBug:1017278) (Ales Kozumplik)
- Base.download_packages() must not assume self.progress exists. (Ales Kozumplik)

* Mon Oct 7 2013 Aleš Kozumplík <ales@redhat.com> - 0.4.3-2
- remove: dnf.yum.rpmsack.RPMDBProblem*. (Ales Kozumplik)
- Update some old-style classes. (Ales Kozumplik)
- support 'dnf group remove' (RhBug:1013764) (Ales Kozumplik)
- remove: Base._limit_installonly_pkgs(). (Ales Kozumplik)
- tests: latest libcomps version has a GroupID objects for env.option_ids. (Ales Kozumplik)
- doc: 'group info'. (RhBug:1013773) (Ales Kozumplik)
- groups: add support for 'dnf group info' (Ales Kozumplik)
- tests: add a group that reflects our other testing packages. (Ales Kozumplik)
- packaging: require GTE versions of dependencies. (Ales Kozumplik)
- cosmetic: trailing whitespace (Ales Kozumplik)
- Fix error handling in Base.install and YumBaseCli.installPkgs. (Radek Holy)
- Fix error handling in Base.remove and YumBaseCli.erasePkgs. (Radek Holy)
- Fix error handling in Base.update and YumBaseCli.updatePkgs. (Radek Holy)
- Fix error handling in Base.downgrade and YumBaseCli.downgradePkgs. (Radek Holy)
- tests: reenable the repo cost testing again. (Ales Kozumplik)
- tests: cleanups in support.py (Ales Kozumplik)

* Tue Oct 1 2013 Aleš Kozumplík <ales@redhat.com> - 0.4.2-1.gitc1716d7
- always enable LRO_FASTESTMIRROR (Zdenek Pavlas)
- progress: add "err" argument to end() callback, merge with failure() (Zdenek Pavlas)
- progress: reformat and reword docstrings (Zdenek Pavlas)
- config: extract prepend_installroot() to a public method. (Ales Kozumplik)
- refactor: Rename exceptions raised by Base.reinstall. (Radek Holy)
- Fix error handling in YumBaseCli.reinstallPkgs. (Radek Holy)
- Fix error handling in Base.reinstall. (Radek Holy)
- refactor: Adapt Base.reinstall to require the same parameters as similar methods. (Radek Holy)
- refactor: Adapt Base.update to require same parameters as similar methods. (Radek Holy)
- add "size" arg to cb.end and cb.failure callbacks (Zdenek Pavlas)
- progress display: handle 100% case better (Zdenek Pavlas)
- progress display: sanitize negative size deltas (Zdenek Pavlas)
- support librepo.PackageTarget(endcb=...) (Zdenek Pavlas)
- remove: Requires urlgrabber (Zdenek Pavlas)
- remove: base.verifyPkg(), base.verifyChecksum() (Zdenek Pavlas)
- remove: urlgrabber.grabber.default_grabber.opts.user_agent (Zdenek Pavlas)
- remove: set_failure_callback() (Zdenek Pavlas)
- update AUTHORS (Ales Kozumplik)
- added assignment of cost option to hawkey repo object (Jan Silhan)
- created new private method _get_installed from code in assertResult (Jan Silhan)
- use librepo.download_packages() (Zdenek Pavlas)
- make repo._local_origin public, as repo.local (Zdenek Pavlas)
- unit tests: dnf.cli.progress (Zdenek Pavlas)
- add dnf.cli.progress (Zdenek Pavlas)
- drop per-repo interrupt callback (Zdenek Pavlas)
- unit tests: dnf.cli.format (Zdenek Pavlas)
- move format_number, format_time to dnf.cli.format (Zdenek Pavlas)
- Fix downgrade inaction if package version provided. (Radek Holy)

* Mon Sep 16 2013 Aleš Kozumplík <ales@redhat.com> - 0.4.1-1.git55e6369
- logging: do not show 'Downloading packages:' on remove. (RhBug:1008444) (Ales Kozumplik)
- remove: couple of config options (kernelpkgnames, exactarch, rpm_check_debug). (Ales Kozumplik)
- remove: dnf.yum.config.mirrorlist_expire, it's unused. (Ales Kozumplik)
- The Fedora .repo files no longer use mirrorlist= for metalink. (Ales Kozumplik)
- leaner .gitignore. (Ales Kozumplik)
- Add Base.reset(). (Ales Kozumplik)
- reimplement urlopen() on top of librepo (Zdenek Pavlas)
- Add '--nocrypto' tsflag config value. (Ales Kozumplik)
- logging: TransactionDisplay.errorlog() logs to stderr. (Ales Kozumplik)
- Until urlbrabber is gone completely, the urlgrabber.progress must stay. (Ales Kozumplik)
- remove all users of urlgrabber.progress.TerminalLine() (Zdenek Pavlas)
- remove all users of urlgrabber.progress.format_time() (Zdenek Pavlas)
- remove all users of urlgrabber.progress.format_number() (Zdenek Pavlas)
- remove all users of urlgrabber.progress.terminal_width_cached() (Zdenek Pavlas)
- remove all users of urlgrabber.grabber.default_grabber (Zdenek Pavlas)
- makecache: do not run makecache on the LiveCD. (Ales Kozumplik)
- doc: what to do on failing %preun. (Ales Kozumplik)
- Fix TypeError raised when _enc called with None (RhBug:1003220) (Radek Holy)

* Fri Aug 30 2013 Aleš Kozumplík <ales@redhat.com> - 0.4.0-1.gitbfccb5c
- Adapt to librepo-1.0.0, handle.url is handle.urls now. (Ales Kozumplik)
- comps: adapt to changes in libcomps handling of env.group_ids. (Ales Kozumplik)
- logging: start and stop of the actual RPM transaction. (Ales Kozumplik)
- logging: nicer logging during transaction. (Ales Kozumplik)
- repo: use all mirrors/baseurls when downloading a package. (Ales Kozumplik)
- logging: log failed checksum check in verifyLocalPkg() (Ales Kozumplik)
- strings: fix suggestion to clean metadata to use 'dnf' (RhBug:997403) (Ales Kozumplik)
- compos: add group.visible property. (Ales Kozumplik)
- tests: comps.environment.group_ids and environment.option.ids. (Ales Kozumplik)
- logging: log when Repo.load() is about to download from remote. (Ales Kozumplik)
- Librepo API changes (Zdenek Pavlas)
- packaging: add libcomps to requires before somebody tries to build this without. (Ales Kozumplik)
- fix: traceback after a merge error, missing comps import. (Ales Kozumplik)
- remove: Repo.base_persistdir. (Ales Kozumplik)
- YumConf: make config_file_age always defined. (Ales Kozumplik)
- make what Base.build_transaction() returns and raises more sane. (Ales Kozumplik)
- remove: dnf.yum.rpmtrans._WrapNoExceptions (Ales Kozumplik)
- transaction displays: report when the TRANS_POST phase starts. (Ales Kozumplik)
- rename: RPM transaction callback hierarchy has now a common name: TransactionDisplay. (Ales Kozumplik)
- Stop the transaction callback's event() accepting both string and id for the action. (Ales Kozumplik)
- Drastically slim down dnf.rpmUtils.arch (Ales Kozumplik)
- refactor: rename: transaction callbacks in rpmtrans.py (Ales Kozumplik)
- remove: dnf.cli.output.CacheProgressCallback. (Ales Kozumplik)
- remove: Config.cache. (Ales Kozumplik)
- logging tweaks. (Ales Kozumplik)
- api: let Base.select_group() take pkg_types. (Ales Kozumplik)
- getter/setter for config.releasever (it is part of the yumvar). (Ales Kozumplik)
- better streamline how conf.yumvar is created and initialized. (Ales Kozumplik)
- add default depsloving callback. (Ales Kozumplik)
- rename: base.dsCallback -> base.ds_callback (Ales Kozumplik)
- rename: DepSolveProgressCallback.pkgAdded()->DepSolveProgressCallback.pkg_added() (Ales Kozumplik)
- comps: *_by_pattern counterparts to *_by_patterns. (Ales Kozumplik)
- comps: better environments and categories support. (Ales Kozumplik)
- tests: basic environemnt parsing works in libcomps now. (Ales Kozumplik)
- tests: there's no dnf.yum.comps any more. (Ales Kozumplik)
- doc: group commands. (Ales Kozumplik)
- remove: dnf.yum.comps. (Ales Kozumplik)
- refactor: GroupsError and CompsException are now both CompsError (Ales Kozumplik)
- comps: rename: group.langonly -> group.lang_only. (Ales Kozumplik)
- comps: implement Group.ui_name (Ales Kozumplik)
- comps: adapt Base.group_lists() to the new comps interface. (Ales Kozumplik)
- libcomps: rename: comps.returnGroups()->comps.groups_by_pattern(). (Ales Kozumplik)
- libcomps: support Base.select_groups() through the new comps. (Ales Kozumplik)
- tests: sort tests in LibcompsTest better. (Ales Kozumplik)
- libcomps: add Comps.groups_by_pattern(). (Ales Kozumplik)
- libcomps: measuring the size of the comps objects. (Ales Kozumplik)
- drop 'overwrite_groups' config option. (Ales Kozumplik)
- libcomps: tests: add sanity test for GH issue 12. (Ales Kozumplik)
- libcomps: add conditional packages. (Ales Kozumplik)
- libcomps: add dnf.comps (wrapper) and a basic UT. (Ales Kozumplik)
- cosmetic: reorder the imports in base.py and cli.py to match the Hacking guidelines[1] (Ales Kozumplik)

* Tue Aug 13 2013 Aleš Kozumplík <ales@redhat.com> - 0.3.11-1.git7d717c7
- fix: UnicodeDecodeError during group install (RhBug:996138) (Ales Kozumplik)
- doc: update the README, move it to .rst (Ales Kozumplik)
- doc: dnf.conf.8 missing from the RPM. (Ales Kozumplik)
- remove: TODO file (Ales Kozumplik)
- output: in list_transaction() list the active transaction members. (RhBug:977753) (Ales Kozumplik)
- rename: Output.listTransaction() -> list_transaction(). (Ales Kozumplik)
- doc: 'best' config option. (Ales Kozumplik)
- repo: do not let librepo resolve mirrorlists on each package download. (RhBug:979042) (Ales Kozumplik)
- remove: mdpolicy and mddownloadpolicy from config. (Ales Kozumplik)
- The DNF default multilib policy is 'best'. (Ales Kozumplik)
- fix: typo in subj.get_best_query() call. (Ales Kozumplik)

* Mon Jul 22 2013 Aleš Kozumplík <ales@redhat.com> - 0.3.10-1.giteb9dddb
- repos: skip_if_unavailable is True by default now. (RhBug:984483) (Ales Kozumplik)
- doc: omitted from 6f70d2b, also mention the related bugzillas. (Ales Kozumplik)
- doc: why 'dnf provides /bin/python' fails on Fedora. (Ales Kozumplik)

* Thu Jul 4 2013 Aleš Kozumplík <ales@redhat.com> - 0.3.9-1.giteff4c49
- fix: errors handling messages in do_transaction(). (RhBug:981310) (Ales Kozumplik)
- fix: typo in 2b4c085 (Ales Kozumplik)
- fix: unhandled OSError exceptions if MD was renewed during transaction (RhBug:980227) (Ales Kozumplik)
- remove: update_md.py (Ales Kozumplik)
- fix: traceback expiring no longer valid repos. (RhBug:979942) (Ales Kozumplik)
- fix: traceback: accessing base.history from download_packages(). (Ales Kozumplik)
- api: Base.build_repo factory method. (Ales Kozumplik)
- python3: absolute imports in cli.main (Ales Kozumplik)
- refactor: KeyboardInterrupt handling in cli.main. (Ales Kozumplik)
- repo: pass substituting variables down into librepo's Handle. (RhBug:964584) (Ales Kozumplik)

* Mon Jun 24 2013 Aleš Kozumplík <ales@redhat.com> - 0.3.8-1.git85524ae
- fix: tracebacks when installing to an empty installroot (RhBug:975858) (Ales Kozumplik)
- doc: 'dnf erase kernel' erases all the kernels. (Ales Kozumplik)
- i18n: even if we have a legit encoding, don't assume it covers the entire UCD (RhBug:976652) (Ales Kozumplik)
- stray self._filelists in Sack. (Ales Kozumplik)
- fix: traceback on check-update when there's a repo without any source. (RhBug:974866) (Ales Kozumplik)
- fix: missing os import in i18n.py (RhBug:974427) (Ales Kozumplik)
- fix: traceback for a regular user when /var/lib/dnf/uuid is not world-readable. (Ales Kozumplik)
- put user locks in /run/user/$UID/dnf. (Ales Kozumplik)
- Minimally teach dnf about rpm rpm >= 4.10 scriptlet start and stop callbacks (Panu Matilainen)
- remove: unnecessary testing for prehistoric rpm versions in callback (Panu Matilainen)
- remove: unused rpmtrans internal _dopkgtup() helper (Panu Matilainen)
- remove: unused rpm repackaging support remnants (Panu Matilainen)
- locking: as an example introduce rpmdb_lock and metadata_cache_lock. (Ales Kozumplik)
- locking: remove the old global locking code. (Ales Kozumplik)
- locking: implement and test ProcessLock class. (Ales Kozumplik)
- Add base_url arg to librepo.download(). (RhBug:968159) (Zdenek Pavlas)
- remove: unused miscutils.compareVerOnly() (Panu Matilainen)
- remove: unused miscutils.stringToVersion() and .flagToString() (Panu Matilainen)
- remove: unused string_to_prco_tuple() and imports used only by it (Panu Matilainen)
- remove: unused miscutils.rpmOutToStr() (Panu Matilainen)
- remove: miscutils.formatRequire() (Panu Matilainen)
- remove: miscutils.rangeCompare() and rangeCheck() (Panu Matilainen)
- remove: miscutils.pkgTupleFromHeader() (Panu Matilainen)
- remove: rpmUtils.TransactionWrapper.returnLeafNodes() method (Panu Matilainen)
- doc: what 'list recent' does. (Ales Kozumplik)
- Resurrect "list recent" functionality (RhBug:908491) (Panu Matilainen)
- doc: add bug summaries to the release notes. (Ales Kozumplik)

* Wed May 29 2013 Aleš Kozumplík <ales@redhat.com> - 0.3.7-1.gitf8bdc98
- ensure the cachedir in Persistor._expired_repos(). (RhBug:967732) (Ales Kozumplik)
- do not load available repositories into the sack for the erase command. (RhBug:916662) (Ales Kozumplik)
- Take out the bulk of YumBaseCli.doTransaction() and put in in Base.do_transaction(). (Ales Kozumplik)
- add noop NoOutputCallback.verify_tsi_package(). (Ales Kozumplik)
- implement dnf.repo.Repo.__repr__(). (Ales Kozumplik)
- output: show the RPMDB alternation warning on debug level only. (Ales Kozumplik)

* Mon May 27 2013 Aleš Kozumplík <ales@redhat.com> - 0.3.6-1.git24ce938
- make the dnf.Base object a context manager. (Ales Kozumplik)
- de-support YUMPDB, not used. (Ales Kozumplik)
- persistent data about repositories should be in cachedir. (Ales Kozumplik)
- YumRPMTransError: use sensible e.value (RhBug:966372) (Zdenek Pavlas)
- store and use information about forced repo expiry (RhBug:965410) (Ales Kozumplik)
- update LibrepoCallbackAdaptor. (RhBug:963627) (Zdenek Pavlas)
- repo: do not try to download or erase packages from a local repo. (RhBug:965114) (Ales Kozumplik)
- tests: weaken the assertion in test_toplevel(). (Ales Kozumplik)
- fix: traceback on 'dnf group install i-dont-exist'. (RhBug:964467) (Ales Kozumplik)
- Handle exceptions in Repo.get_package. (RhBug:963680) (Ales Kozumplik)
- subject parsing: inform the user if given spec matches no package on install. (RhBug:963133) (Ales Kozumplik)
- logging: setup provisional logging even before config. (Ales Kozumplik)
- refactor: dnf.logging, put the setup() methods inside a new class, Logging. (Ales Kozumplik)
- provides command: there's no reason to output so many empty lines between matches. (Ales Kozumplik)

* Mon May 13 2013 Aleš Kozumplík <ales@redhat.com> - 0.3.5-1.git85c924f
- recognize 'dnf list upgrades' as an 'dnf list updates' alias. (Ales Kozumplik)
- transaction: add reinstall as a special action. (Ales Kozumplik)
- rename: Base.buildTransaction() -> build_transaction() (Ales Kozumplik)
- remove: dnf.yum.output.pkgname_ui() et al. (Ales Kozumplik)
- remove: dnf/yum/transactioninfo.py (Ales Kozumplik)
- transaction: migrate remaining legit uses of tsInfo before it's purged. (Ales Kozumplik)
- remove: SimpleCliCallBack, _getTxmbr from rpmtrans.py slimming it down. (Ales Kozumplik)
- transactions: fix post_transaction_output(). (Ales Kozumplik)
- transaction: make history work again. (Ales Kozumplik)
- refactor: Base.populate_ts() is now Transaction.populate_rpm_ts(). (Ales Kozumplik)
- rename: verify_pkg() -> verify_tsi_package(). (Ales Kozumplik)
- rename: verifyTransaction() -> verify_transaction() (Ales Kozumplik)
- transactions: reenable transaction verification. (Ales Kozumplik)
- remove: dnf/cli/callback.py, dnf/yum/callbacks.py. (Ales Kozumplik)
- populate_ts: handle obsoleting installs. (Ales Kozumplik)
- transaction: bring rpmtrans.py into a shape where transactions can be tested. (Ales Kozumplik)
- tests: adapt unit tests to dnf.transaction scheme of things. (Ales Kozumplik)
- transaction: migrate YumBaseCli.doTransaction() to dnf.transaction. (Ales Kozumplik)
- transaction: migrate YumOutput.list_transaction() to dnf.transaction. (Ales Kozumplik)
- transaction: rewrite Base.populate_ts() to use dnf.transaction. (Ales Kozumplik)
- transaction: use dnf.transaction instead of dnf.yum.transactioninfo in buildTransaction(). (Ales Kozumplik)
- add dnf.util.group_by_filter() (Ales Kozumplik)
- transaction: foundations of dnf.Transaction and a test. (Ales Kozumplik)
- transactions: do not use TransactionData to store the packaging requests. (Ales Kozumplik)
- tests: rename: test_transaction.py -> test_transactiondata.py (Ales Kozumplik)
- repo: handle reviving exceptions like any other librepo exception. (RhBug:961549) (Ales Kozumplik)
- doc: fix spellings of the distro-sync command. (RhBug:959990) (Ales Kozumplik)

* Thu May 2 2013 Aleš Kozumplík <ales@redhat.com> - 0.3.4-1.git03fd687
- tests: python3 absolute imports. (Ales Kozumplik)
- tests: rename: tests/base.py -> tests/support.py (Ales Kozumplik)
- hawkey commit 8d77592 simplifies detecting obsoleted transaction members. (Ales Kozumplik)
- adapt to hawkey change fe99cd4. (Ales Kozumplik)
- adapt to hawkey changes f8334df and 0fee231 (Goal.obsoleted_by_package et al.) (Ales Kozumplik)
- cli, transaction: recognize and report proper obsoletes. (RhBug:887317) (Ales Kozumplik)
- refactor: get_best_query() and get_best_selector() both accept 'forms' now. (Ales Kozumplik)
- comps: support 'dnf group install'. (Ales Kozumplik)
- repo: integrate API improvements in librepo. (Ales Kozumplik)
- comps: start readding group commands, 'dnf groups summary' works now. (Ales Kozumplik)
- fix invisible 'repolist -v' output. (Ales Kozumplik)
- remove: main() methods from the production code. (Ales Kozumplik)
- cosmetic: remove trailing whitespace in dnf/yum/pgpgmsg.py (Ales Kozumplik)
- tests: do not create repos/gen. (Ales Kozumplik)
- comps: fix up Base.read_comps() and Comps.compile() so the comps loading works. (Ales Kozumplik)
- tests: cosmetics: alphabetically reorder FakeConf items. (Ales Kozumplik)
- doc: protected_packages not supported. (Ales Kozumplik)
- tests: add sanity test for dnf.yum.comps (Ales Kozumplik)
- repo: with timed makecache only try one mirror per repo. (RhBug:922667) (Ales Kozumplik)
- repo: latest librepo needs explicit perform() to get the metalink. (Ales Kozumplik)
- repo: clean mirrorlist files too on 'dnf clean'. (Ales Kozumplik)
- repo: with librepo >= 88c90e3 the "baseurl is the first mirror" hack is gone. (Ales Kozumplik)
- remove: some unused arch-related methods from dnf.yum.base (Ales Kozumplik)
- fix typo in the spec. (Ales Kozumplik)

* Wed Apr 17 2013 Aleš Kozumplík <ales@redhat.com> - 0.3.3-3.git91ba5e0
- packaging: do not run 'systemctl' to enable the timer service manually. (Ales Kozumplik)
- cosmetic: trailing whitespace in dnf/cli/callback.py (Ales Kozumplik)
- UI: call updates upgrades. (RhBug:903775) (Ales Kozumplik)
- doc: the logging setup. (Ales Kozumplik)
- logging: in logfiles, mark the start of the logging session. (Ales Kozumplik)
- logging: replace setup_from_dnf_levels with a helpers that takes the conf object. (Ales Kozumplik)
- put the name of the loglevel into the logfiles (Ales Kozumplik)
- logging: do not do logging.basicConfig() from CLI. (Ales Kozumplik)
- remove: dnf.const.LOG_TRANSACTION no longer needed. (Ales Kozumplik)
- doc: fix documentation build. (Ales Kozumplik)
- remove: dnf.yum.logginglevels (Ales Kozumplik)
- finally, setup logging via the new module. (Ales Kozumplik)
- Migrate the remaining DEBUG_3 and DEBUG_4 levels. (Ales Kozumplik)
- semi-automatically migrate the old logging levels to the new ones. (Ales Kozumplik)
- Fix how checking whether the CLI is verbose is done. (Ales Kozumplik)
- Use the new DNF loggers instead of the old ones. (Ales Kozumplik)
- add the logger for rpm transactions. (Ales Kozumplik)
- tests: unified stdout/stderr patching. (Ales Kozumplik)
- implement dnf.logging module (Ales Kozumplik)
- refactor: add absolute imports some places so I can have dnf.logging module. (Ales Kozumplik)
- fix traceback with 'dnf history info <number>'. (Ales Kozumplik)
- cosmetic: trailing whitespace in comps.py (Ales Kozumplik)
- refactor: use print() the python3 function-style. (Ales Kozumplik)
- rename: dnf.exceptions.YumBaseError to dnf.exceptions.Error. (Ales Kozumplik)
- move: dnf.yum.Errors to dnf.exceptions. (Ales Kozumplik)
- remove deprecation exceptions and warnings. (Ales Kozumplik)
- remove: dnf/yum/mdparser.py (Ales Kozumplik)
- remove: unused exception classes. (Ales Kozumplik)
- remove: dnf/yum/repoMDObject.py (Ales Kozumplik)

* Mon Apr 8 2013 Aleš Kozumplík <ales@redhat.com> - 0.3.2-1.gitf3818b4
- remove: dnf.yum.failover. (Ales Kozumplik)
- 'reviving' repositories using checksum information from metalink. (Ales Kozumplik)
- dnf.util.touch() accepts 'no_create' parameter now. (Ales Kozumplik)
- refactor: repo: move checking of existing metadata from _try_cache() to load(). (Ales Kozumplik)
- refactor: put Repo.load() at the correct place in the class. (Ales Kozumplik)
- refactor: call repo._Result what it really is: Metadata. (Ales Kozumplik)
- 'repolist -v' shows the mirrorlists now. (Ales Kozumplik)
- tests: specify debug_solver in FakeConf too. (Ales Kozumplik)
- debugging: add '--debugsolver' CLI switch. (Ales Kozumplik)
- doc: the excludes behavior (RhBug:947258) (Ales Kozumplik)
- doc: fix failing documentation build after dnf.yum.metalink is gone. (Ales Kozumplik)
- fix configuration of per-repo excludes. (Ales Kozumplik)
- tests: repo handle: test the useragent string. (Ales Kozumplik)
- remove: dnf.yum.metalink. (Ales Kozumplik)
- remove: ResolveDepCommand. (Ales Kozumplik)
- support repo.skip_if_unavailable config option. (RhBug:889202) (Ales Kozumplik)
- refactor: base.sack is no longer a lazy attribute. (Ales Kozumplik)
- nicer error reporting in repo.py. (Ales Kozumplik)
- Enable 'interruptible' for librepo operations. (Ales Kozumplik)
- set user agent for librepo communication too. (RhBug:923384) (Ales Kozumplik)
- fix superfluous 'None' in the error output. (Ales Kozumplik)
- don't be pompous about the newlines in error messages. (Ales Kozumplik)
- fix traceback with --enablerepo=<repo> and an unknown repo <repo>. (Ales Kozumplik)
- logging: journald was getting the wrong idea about the program name. (Ales Kozumplik)
- debugging: output the package metadata on '--debugrepodata'. (Ales Kozumplik)
- fix traceback in UpgradeToCommand.doCheck(). (Ales Kozumplik)
- also start the dnf-makecache.timer on installation. (Ales Kozumplik)

* Thu Mar 28 2013 Aleš Kozumplík <ales@redhat.com> - 0.3.1-3.git7b1d503
- makecache: no on_ac_power binary means we should go ahead anyway. (Ales Kozumplik)
- packaging: run systemd scriptlets so the timer service can be enabled by default. (Ales Kozumplik)
- :doc release notes - the metadata_expire default has changed. (Ales Kozumplik)
- :doc start making release notes. (Ales Kozumplik)
- abrt: change the event to post-create so journalctl works (post-create runs under root) (Ales Kozumplik)
- :doc clean_requiremennts_on_remove on by default. (Ales Kozumplik)
- logging: put a log file marker on each run, nicer 'Ext Commands' output. (Ales Kozumplik)
- :doc explain how timed metadata syncing can be tweaked and disabled. (Ales Kozumplik)
- Do not execute the timer makecache when running on a battery. (RhBug:919769) (Ales Kozumplik)
- :doc create dnf.config, describe 'metadata_timer_sync'. (Ales Kozumplik)
- config defaults: timer makecache every 3 hours, bump default md expiry to 48 hours. (RhBug:892064) (Ales Kozumplik)
- mechanism for disabling or changing the period of automatic metadata syncing. (RhBug:922664) (Ales Kozumplik)
- run the regular makecache from a systemd timer (RhBug:878826) (Ales Kozumplik)
- stop using the obsoleted repo.cache property (RhBug:926871) (Ales Kozumplik)
- userconfirm() mustn't fail on EOFError. (RhBug:922521) (Ales Kozumplik)
- :doc document --nogpgcheck and --releasever. (Ales Kozumplik)
- :doc remove yum.repos and yum.yumRepo from the obsoleted API documentation. (Ales Kozumplik)
- :doc sort CLI options alphabetically. (Ales Kozumplik)
- Downgrade only once if multiple old versions are available. (RhBug:921294) (Ales Kozumplik)
- :refactor, improve base.ts management, use properties. (Ales Kozumplik)
- Filter rpm.RPMPROB_FILTER_OLDPACKAGE for all transactions whatsover (RhBug:916657) (Ales Kozumplik)
- :tests :move test_yumbase.py -> test_base.py (Ales Kozumplik)
- remove: finally drop yum/repos.py and yum/yumRepo.py (Ales Kozumplik)

* Thu Mar 21 2013 Aleš Kozumplík <ales@redhat.com> - 0.3.0-2.git3e52d13
- repo: use shutil.move instead of os.rename (Ales Kozumplik)

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
- massive dead code removals across the code base (3k LOC dropped)
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
