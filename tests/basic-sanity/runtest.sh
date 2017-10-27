#!/bin/bash
# vim: dict+=/usr/share/beakerlib/dictionary.vim cpt=.,w,b,u,t,i,k
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   runtest.sh of /CoreOS/dnf/Sanity/basic-sanity
#   Description: basic sanity test
#   Author: Eva Mrakova <emrakova@redhat.com>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Copyright (c) 2017 Red Hat, Inc.
#
#   This program is free software: you can redistribute it and/or
#   modify it under the terms of the GNU General Public License as
#   published by the Free Software Foundation, either version 2 of
#   the License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be
#   useful, but WITHOUT ANY WARRANTY; without even the implied
#   warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
#   PURPOSE.  See the GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program. If not, see http://www.gnu.org/licenses/.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Include Beaker environment
. /usr/bin/rhts-environment.sh || exit 1
. /usr/share/beakerlib/beakerlib.sh || exit 1

PACKAGE="dnf"

DNF_CMD="dnf --disablerepo=\* --enablerepo=tstrepo\*"

RPMS="/root/rpmbuild/RPMS/noarch"
REPO="/var/www/html/tstrepo"

pkgtorepo() {
    # builds a .rpm from given .spec, moves it to a testrepo identified by index
    # $1 ... pkgname, $2 ... tstrepo index
    rpmbuild -bb ${1}.spec &> /dev/null
    cp $RPMS/${1}*.rpm ${REPO}${2}
    rm -f $RPMS/${1}*.rpm
}

rlJournalStart
    rlPhaseStartSetup
        rlAssertRpm $PACKAGE
        rlFileBackup --clean /etc/yum.repos.d/ /var/log/httpd/
        rlRun "TmpDir=\$(mktemp -d)" 0 "Creating tmp directory"
        rlRun "cp *.spec $TmpDir"
        rlRun "pushd $TmpDir"
        for i in {1..2}; do
            rlRun "mkdir $REPO$i" 0 "Create dir for tstrepo$i"
            cat > /etc/yum.repos.d/tstrepo${i}.repo <<EOF
[tstrepo$i]
name=tstrepo$i
baseurl=http://localhost/tstrepo$i/
enabled=1
gpgcheck=0
EOF
        done
        pkgtorepo testA 1
        rlRun "createrepo_c ${REPO}1" 0 "Create tstrepo1"
        rlRun "createrepo_c ${REPO}2" 0 "Create tstrepo2"

        # workaround: when /var/log/httpd does not exist, httpd fails to start
        if [[ ! -d /var/log/httpd ]]; then mkdir -p /var/log/httpd; fi 
        rlServiceStart httpd
    rlPhaseEnd

    rlPhaseStartTest "Install, upgrade, downgrade and remove a pkg without dependencies"
        # install a single pkg
        rlRun "$DNF_CMD -y install testA" 0 "Install testA"
        rlAssertRpm testA 1
        # upgrade the pkg
        rlRun "sed -i 's/Version.*$/Version: 2/' testA.spec"
        pkgtorepo testA 2
        rlRun "createrepo_c ${REPO}2" 0 "Update tstrepo2"
        rlRun "$DNF_CMD clean all" 0 "Clean dnf cache"
        rlRun "$DNF_CMD -y upgrade testA" 0 "Upgrade testA"
        rlAssertRpm testA 2
        # downgrade the pkg
        rlRun "$DNF_CMD -y downgrade testA" 0 "Downgrade testA"
        rlAssertRpm testA 1
        # remove the pkg
        rlRun "$DNF_CMD -y remove testA" 0 "Remove testA"
        rlAssertNotRpm testA
    rlPhaseEnd

    rlPhaseStartTest "Install and remove a pkg with dependencies"
        # prepare data
        pkgtorepo testB 2
        pkgtorepo testC 2
        rlRun "createrepo_c ${REPO}2" 0 "Update tstrepo2"
        rlRun "$DNF_CMD clean all" 0 "Clean dnf cache"
        # install a pkg (B depends on C, C depends on A)
        rlRun "$DNF_CMD -y install testB" 0 "Install testB and its deps"
        rlAssertRpm testB 1
        rlAssertRpm testC 1
        rlAssertRpm testA 2
        # remove the pkg (C and B should be removed)
        rlRun "$DNF_CMD -y --setopt clean_requirements_on_remove=0 remove testC" 0 "Remove testC"
        rlAssertNotRpm testC
        rlAssertNotRpm testB
        # testA should not be removed as an unused dep
        rlAssertRpm testA 2
    rlPhaseEnd

    rlPhaseStartTest "Getting info (list, info, search, provides, whatprovides)"
        # list
        rlRun "$DNF_CMD list installed test\* > list1.out" 0 "Run dnf list installed"
        rlAssertGrep "testA.*noarch" list1.out
        rlAssertNotGrep "testB.*noarch" list1.out
        rlAssertNotGrep "testC.*noarch" list1.out
        rlRun "$DNF_CMD list available test\* > list2.out" 0 "Run dnf list available"
        rlAssertGrep "testB.*noarch" list2.out
        rlAssertGrep "testC.*noarch" list2.out
        rlAssertNotGrep "testA.*noarch" list2.out
        rlRun "$DNF_CMD -y downgrade testA" 0 "Downgrade testA"
        rlRun "$DNF_CMD list upgrades > list3.out" 0 "Run dnf list upgrades"
        rlAssertGrep "testA.*noarch.*tstrepo2" list3.out
        # info
        rlRun "$DNF_CMD info test[B-Z] > info.out" 0 "Run dnf info"
        rlAssertGrep "Name.*testB" info.out
        rlAssertGrep "Name.*testC" info.out
        rlAssertNotGrep "Name.*testA" info.out
        # search
        rlRun "$DNF_CMD search 'This is a testB' > search.out" 0 "Run dnf search"
        rlAssertGrep "Matched: This is a testB" search.out
        rlAssertGrep "testB.*noarch" search.out
        # provides
        rlRun "$DNF_CMD provides testC-provides > provides.out" 0 "Run dnf provides"
        rlAssertGrep "testC.*noarch" provides.out
        # whatprovides
        rlRun "$DNF_CMD whatprovides '/usr/bin/testA' > provides2.out" 0 "Run dnf whatprovides"
        rlAssertGrep "testA-1.*noarch" provides2.out
        rlAssertGrep "testA-2.*noarch" provides2.out
    rlPhaseEnd

    rlPhaseStartTest "History (list, info, undo, redo)"
        rlRun "$DNF_CMD history list > hist1.out" 0 "Run dnf history list"
        rlAssertGrep "Downgrade" hist1.out
        # last transaction was testA downgrade, let's get its ID
        rlRun "$DNF_CMD history info > hist2.out" 0 "Run dnf history info"
        DOWNGRADE_HIST_ID=$(grep 'Transaction ID' hist2.out | cut -d: -f2)
        rlRun "$DNF_CMD -y history undo last" 0 "Run dnf history undo"
        rlAssertRpm testA 2
        rlRun "$DNF_CMD -y history redo $DOWNGRADE_HIST_ID" 0 "Run dnf history redo"
        rlAssertRpm testA 1
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "$DNF_CMD -y remove testA"
        rlRun "rm -rf /var/www/html/tstrepo{1,2}" 0 "Delete tstrepo dirs"
        rlRun "$DNF_CMD clean all" 0 "Clean dnf cache"
        rlFileRestore
        rlServiceRestore httpd
        rlRun "popd"
        rlRun "rm -r $TmpDir" 0 "Remove tmp directory"
    rlPhaseEnd
rlJournalPrintText
rlJournalEnd
