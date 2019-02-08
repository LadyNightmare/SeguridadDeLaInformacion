/* vi: set sw=4 ts=4:
 *
 * Copyright (C) 2001 - 2012 Christian Hohnstaedt.
 *
 * All rights reserved.
 */

#include "lib/func.h"
#include "Options.h"
#include "SearchPkcs11.h"
#include "lib/pki_scard.h"
#include <openssl/objects.h>
#include <QMessageBox>
#include <QToolTip>

Options::Options(MainWindow *parent)
	:QDialog(parent)
{
	mw = parent;

	setWindowTitle(XCA_TITLE);
	setupUi(this);

	foreach(int nid, *MainWindow::dn_nid) {
		QString n = OBJ_nid2ln(nid);
		extDNobj->addItem(n);
		expDNobj->addItem(n);
	}
	string_opts << "MASK:0x2002" << "pkix" << "nombstr" <<
			"utf8only" << "default";
	QStringList s;
	s << tr("Printable string or UTF8 (default)")
	  << tr("PKIX recommendation in RFC2459")
	  << tr("No BMP strings, only printable and T61")
	  << tr("UTF8 strings only (RFC2459)")
	  << tr("All strings");
	mbstring->addItems(s);
	mbstring->setCurrentIndex(string_opts.indexOf(Settings["string_opt"]));

	searchP11 = NULL;
	transDnEntries->setText(transDnEntries->text()
			.arg(OBJ_nid2ln(NID_commonName))
			.arg(dn_translations[NID_commonName]));

	setDnString(Settings["mandatory_dn"], extDNlist);
	setDnString(Settings["explicit_dn"], expDNlist);
	setupPkcs11Provider(Settings["pkcs11path"]);

	suppress->setCheckState(Settings["suppress_messages"]);
	noColorize->setCheckState(Settings["no_expire_colors"]);
	transDnEntries->setCheckState(Settings["translate_dn"]);
	onlyTokenHashes->setCheckState(Settings["only_token_hashes"]);
	disableNetscape->setCheckState(Settings["disable_netscape"]);
	adapt_explicit_subject->setCheckState(Settings["adapt_explicit_subject"]);

	QStringList units;
	QString x = Settings["ical_expiry"];

	units << tr("Days") << "D" << tr("Weeks") << "W";
	ical_expiry_unit->addItemsData(units, x.right(1));
	x.chop(1);
	ical_expiry_num->setText(x);

	units << "%" << "%";
	x = QString(Settings["cert_expiry"]);
	cert_expiry_unit->addItemsData(units, x.right(1));
	x.chop(1);
	cert_expiry_num->setText(x);

	serial_len->setValue(Settings["serial_len"]);
}

Options::~Options()
{
	if (searchP11)
		delete searchP11;
}

void Options::on_extDNadd_clicked()
{
	extDNlist->addItem(extDNobj->currentText());
}

void Options::on_extDNdel_clicked()
{
	extDNlist->takeItem(extDNlist->currentRow());
}

void Options::on_expDNadd_clicked()
{
	expDNlist->addItem(expDNobj->currentText());
}

void Options::on_expDNdel_clicked()
{
	expDNlist->takeItem(expDNlist->currentRow());
}

void Options::on_expDNdefault_clicked()
{
	setDnString(Settings.defaults("explicit_dn"), expDNlist);
}

void Options::setDnString(QString dn, QListWidget *w)
{
	QStringList dnl;

	if (!dn.isEmpty())
		dnl = dn.split(",");
	w->clear();
	for (int i=0; i < dnl.count(); i++) {
		int nid = OBJ_sn2nid(CCHAR(dnl[i]));
		w->addItem(OBJ_nid2ln(nid));
	}
}

QString Options::getDnString(QListWidget *w)
{
	QStringList dn;

	for (int j=0; j<w->count(); j++) {
		int nid = OBJ_ln2nid(CCHAR(w->item(j)->text()));
		dn << QString(OBJ_nid2sn(nid));
	}
	return dn.join(",");
}

int Options::exec()
{
	if (QDialog::exec() == QDialog::Rejected)
		return QDialog::Rejected;

	Transaction;
	if (!TransBegin())
		return QDialog::Rejected;

	Settings["suppress_messages"] = suppress->checkState();
	Settings["no_expire_colors"] = noColorize->checkState();
	Settings["translate_dn"] = transDnEntries->checkState();
	Settings["only_token_hashes"] = onlyTokenHashes->checkState();
	Settings["disable_netscape"] = disableNetscape->checkState();

	Settings["default_hash"] = hashAlgo->currentHashName();
	Settings["mandatory_dn"] = getDnString(extDNlist);
	Settings["explicit_dn"] = getDnString(expDNlist);
	Settings["string_opt"] = string_opts[mbstring->currentIndex()];
	Settings["pkcs11path"] = getPkcs11Provider();

	Settings["cert_expiry"] = cert_expiry_num->text() +
				cert_expiry_unit->currentItemData().toString();
	Settings["ical_expiry"] = ical_expiry_num->text() +
				ical_expiry_unit->currentItemData().toString();
	Settings["serial_len"] = serial_len->value();
	Settings["adapt_explicit_subject"] = adapt_explicit_subject->checkState();

	return TransCommit() ? QDialog::Accepted : QDialog::Rejected;
}

void Options::on_addButton_clicked(void)
{
	load_pkcs11 l;
	QString fname;

	fname = QFileDialog::getOpenFileName(this, l.caption,
		getLibDir(), l.filter);

	addLib(fname);
}

void Options::addLib(QString fname)
{
	pkcs11_lib *lib;
	QString status;

	fname = QFileInfo(fname).canonicalFilePath();

	if (fname.isEmpty() || pkcs11::get_lib(fname))
		return;
	try {
		lib = pkcs11::load_lib(fname, false);
		if (lib)
			status = lib->driverInfo();
	} catch (errorEx &ex) {
		lib = NULL;
		status = ex.getString();
	}
	status = status.trimmed();
	QListWidgetItem *item = new QListWidgetItem(fname);
	item->setToolTip(status);
	if (lib)
		item->setIcon(*MainWindow::doneIco);
	pkcs11List->addItem(item);
	if (searchP11)
		QToolTip::showText(searchP11->mapToGlobal(
			QPoint(0,0)), status);
}

void Options::on_removeButton_clicked(void)
{
	QListWidgetItem *item = pkcs11List->takeItem(pkcs11List->currentRow());
	if (!item)
		return;
	try {
		pkcs11::remove_lib(item->text());
	} catch (errorEx &err) {
		mw->Error(err);
	}
}

void Options::on_searchPkcs11_clicked(void)
{
	if (!searchP11) {
		searchP11 = new SearchPkcs11(this, QString());
		connect(searchP11, SIGNAL(addLib(QString)),
			this, SLOT(addLib(QString)));
	}
	searchP11->show();
}

void Options::setupPkcs11Provider(QString list)
{
	pkcs11_lib_list libs = pkcs11::get_libs();

	foreach(pkcs11_lib *l, libs) {
		QListWidgetItem *item = new QListWidgetItem(l->filename());
		try {
			item->setToolTip(l->driverInfo());
			item->setIcon(*MainWindow::doneIco);
		} catch (errorEx &err) {
			mw->Error(err);
		}
		pkcs11List->addItem(item);
	}
	if (!list.isEmpty()) {
		foreach(QString libname, list.split('\n')) {
			if (libs.get_lib(libname))
				continue;
			QListWidgetItem *item = new QListWidgetItem(libname);
			item->setToolTip(tr("Load failed"));
			pkcs11List->addItem(item);
		}
	}
}

QString Options::getPkcs11Provider()
{
	QStringList prov;
	for (int j=0; j<pkcs11List->count(); j++) {
		prov << pkcs11List->item(j)->text();
	}
	if (prov.count() == 0)
		return QString("");
	return prov.join("\n");
}
