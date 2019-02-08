/* vi: set sw=4 ts=4:
 *
 * Copyright (C) 2001 - 2011 Christian Hohnstaedt.
 *
 * All rights reserved.
 */

#include "func.h"
#include "oid.h"
#include "pki_x509super.h"
#include "db_base.h"

QPixmap *pki_x509super::icon[1];

pki_x509super::pki_x509super(const QString name)
	: pki_x509name(name)
{
	privkey = NULL;
}

pki_x509super::~pki_x509super()
{
}

QSqlError pki_x509super::lookupKey()
{
	XSqlQuery q;
	unsigned hash = pubHash();

	SQL_PREPARE(q, "SELECT item FROM public_keys WHERE hash=?");
	q.bindValue(0, hash);
	q.exec();
	if (q.lastError().isValid())
		return q.lastError();
	while (q.next()) {
		pki_key *x = db_base::lookupPki<pki_key>(q.value(0));
		if (!x) {
			qDebug("Public key with id %d not found",
				q.value(0).toInt());
			continue;
		}
		x->resetUcount();
		if (compareRefKey(x)) {
			setRefKey(x);
			break;
		}
	}
	return q.lastError();
}

QSqlError pki_x509super::insertSqlData()
{
	QSqlError e = lookupKey();
	if (e.isValid())
		return e;

	XSqlQuery q;
	SQL_PREPARE(q, "INSERT INTO x509super (item, subj_hash, pkey, key_hash) "
		  "VALUES (?, ?, ?, ?)");
	q.bindValue(0, sqlItemId);
	q.bindValue(1, (uint)getSubject().hashNum());
	q.bindValue(2, privkey ? privkey->getSqlItemId() : QVariant());
	q.bindValue(3, pubHash());
	q.exec();
	return q.lastError();
}

void pki_x509super::restoreSql(const QSqlRecord &rec)
{
	pki_base::restoreSql(rec);
	keySqlId = rec.value(VIEW_x509super_keyid);
        privkey = NULL;
}

QSqlError pki_x509super::deleteSqlData()
{
	XSqlQuery q;
	if (privkey)
		privkey->resetUcount();
	SQL_PREPARE(q, "DELETE FROM x509super WHERE item=?");
	q.bindValue(0, sqlItemId);
	q.exec();
	return q.lastError();
}

pki_key *pki_x509super::getRefKey() const
{
	return privkey;
}

unsigned pki_x509super::pubHash() const
{
	unsigned hash = 0;
	if (privkey) {
		hash = privkey->hash();
	} else {
		pki_key *x = getPubKey();
		if (x) {
			hash = x->hash();
			delete x;
		}
	}
	return hash;
}

bool pki_x509super::compareRefKey(pki_key *ref) const
{
	bool x;

	if (ref == NULL)
		return false;
	pki_key *mk = getPubKey();
	if (mk == NULL)
		return false;
	x = ref->compare(mk);
	delete mk;
	return x;
}

void pki_x509super::setRefKey(pki_key *ref)
{
	privkey = ref;
}

QString pki_x509super::getSigAlg() const
{
	return QString(OBJ_nid2ln(sigAlg()));
}

const EVP_MD *pki_x509super::getDigest()
{
	return EVP_get_digestbynid(sigAlg());
}

bool pki_x509super::hasPrivKey() const
{
	pki_key *k = getRefKey();
	return k && k->isPrivKey();
}

QVariant pki_x509super::getIcon(const dbheader *hd) const
{
	if (hd->id == HD_x509key_name)
		return hasPrivKey() ? QVariant(*icon[0]) : QVariant();

	return pki_base::getIcon(hd);
}

QVariant pki_x509super::column_data(const dbheader *hd) const
{
	if (hd->id == HD_x509key_name) {
		if (!privkey)
			return QVariant("");
		return QVariant(privkey->getIntName());
	}
	if (hd->id == HD_x509_sigalg) {
		return QVariant(getSigAlg());
	}
	if (hd->type == dbheader::hd_v3ext ||
	    hd->type == dbheader::hd_v3ext_ns)
	{
		extList el = getV3ext();
		int idx = el.idxByNid(hd->id);
		if (idx == -1)
			return QVariant("");
		return QVariant(el[idx].getValue(false));
	}
	return pki_x509name::column_data(hd);
}

static QString oid_sect()
{
	QString ret;
	int i, max = OBJ_new_nid(0);

	for (i=first_additional_oid; i < max; i++) {
		const char *sn = OBJ_nid2sn(i);
		if (!sn)
			break;
		ret += QString("%1 = %2\n").
			arg(OBJ_nid2sn(i)).
			arg(OBJ_obj2QString(OBJ_nid2obj(i), 1));
	}

	if (!ret.isEmpty()) {
		ret = QString("oid_section = xca_oids\n\n"
			"[ xca_oids ]\n") + ret + "\n";
	}
	return ret;
}

void pki_x509super::opensslConf(QString fname)
{
	QString extensions;
	extList el = getV3ext();
	x509name n = getSubject();
	el.genGenericConf(&extensions);

	QString name = n.taggedValues();
	QString final = oid_sect();
	final += QString("[ req ]\n"
		"default_bits = 1024\n"
		"default_keyfile = privkey.pem\n"
		"distinguished_name = xca_dn\n"
		"x509_extensions = xca_extensions\n"
		"req_extensions = xca_extensions\n"
		"string_mask = MASK:0x%3\n"
		"utf8 = yes\n"
		"prompt = no\n\n"
		"[ xca_dn ]\n"
		"%1\n"
		"[ xca_extensions ]\n"
		"%2").arg(name).arg(extensions).
			arg(ASN1_STRING_get_default_mask(), 0, 16);

	FILE *fp = fopen_write(fname);
	if (fp == NULL) {
		fopen_error(fname);
		return;
	}
	QByteArray ba = final.toUtf8();
	fwrite_ba(fp, ba, fname);
	fclose(fp);
}

bool pki_x509super::visible() const
{
	if (pki_x509name::visible())
		return true;
	if (getSigAlg().contains(limitPattern))
		return true;
	return getV3ext().search(limitPattern);
}

// Start class  pki_x509name

pki_x509name::pki_x509name(const QString name)
	: pki_base(name)
{
}

void pki_x509name::autoIntName()
{
	x509name subject = getSubject();
	setIntName(subject.getMostPopular());
}

QVariant pki_x509name::column_data(const dbheader *hd) const
{
	switch (hd->id) {
	case HD_subject_name:
		return QVariant(getSubject().oneLine(
				XN_FLAG_ONELINE & ~ASN1_STRFLGS_ESC_MSB));
	case HD_subject_hash:
		return  QVariant(getSubject().hash());
	default:
		if (hd->type == dbheader::hd_x509name)
			return QVariant(getSubject().getEntryByNid(hd->id));
	}
	return pki_base::column_data(hd);
}

bool pki_x509name::visible() const
{
	if (pki_base::visible())
		return true;
	return getSubject().search(limitPattern);
}
