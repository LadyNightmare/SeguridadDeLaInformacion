#include "settings.h"
#include "func.h"
#include "sql.h"
#include "widgets/hashBox.h"
#include "widgets/NewKey.h"
#include <QDir>
#include <QFile>
#include <openssl/asn1.h>

settings Settings;

svalue::svalue(settings *s, const QString &k)
{
	setting = s;
	key = k;
}

QString svalue::get() const
{
	return setting ? setting->get(key) : QString();
}
void svalue::set(const QString &val)
{
	if (setting)
		setting->set(key, val);
}

settings::settings()
{
	defaul["mandatory_dn"] = "";
	defaul["explicit_dn"] = "C,ST,L,O,OU,CN,emailAddress";
	defaul["string_opt"] = "MASK:0x2002";
	defaul["workingdir"] = QDir::toNativeSeparators(QDir::currentPath());
	defaul["default_hash"] = hashBox::getDefault();
	defaul["ical_expiry"] = "1W";
	defaul["cert_expiry"] = "80%";
	defaul["serial_len"] = "64";

	hostspecific << "pkcs11path" << "workingdir" << "mw_geometry";

	clear();
}

void settings::clear()
{
	loaded = false;
	values.clear();
	db_keys.clear();
	foreach(QString key, defaul.keys())
		setAction(key, defaul[key]);
}

void settings::setAction(const QString &key, const QString &value)
{
	if (key == "string_opt")
		ASN1_STRING_set_default_mask_asc((char*)CCHAR(value));
	else if (key == "default_hash")
		hashBox::setDefault(value);
	else if (key == "defaultkey")
		NewKey::setDefault(value);
	else if (key == "optionflags") {
		XSqlQuery q;
		Transaction;
		if (!TransBegin())
			return;
		SQL_PREPARE(q, "DELETE FROM settings where key_='optionflags'");
		q.exec();
		foreach(QString flag, value.split(",")) {
			if (flag == "dont_colorize_expiries")
				flag = "no_expire_colors";
			setAction(flag, "yes");
		}
		TransCommit();
		return;
	}
	values[key] = value;
}

QString settings::defaults(const QString &key)
{
	return defaul[key];
}

void settings::load_settings()
{
	if (loaded || !QSqlDatabase::database().isOpen())
		return;
	XSqlQuery q("SELECT key_, value FROM settings");
	while (q.next()) {
		QString key = q.value(0).toString().simplified();
		QString value = q.value(1).toString().simplified();
		QStringList l = key.split(":");
		if (l.size() == 2 && l[1] != hostId())
			continue;	// Skip key with non-matching host ID
		db_keys << key;		// Key with host ID
		setAction(l[0], value);	// Key without host ID
	}
	loaded = true;
}

QString settings::get(QString key)
{
	load_settings();
	return values.contains(key) ? values[key] : QString();
}

void settings::set(QString key, QString value)
{
	XSqlQuery q;
	load_settings();

	if (key == "workingdir") {
		if (portable_app() || !QDir(value).exists())
			return;
		value = QDir::toNativeSeparators(value);
	}
	if (hostspecific.contains(key))
		key += QString(":%1").arg(hostId());
	if (db_keys.contains(key) && values[key] == value)
		return;

	Transaction;
	if (!TransBegin())
		return;

	if (db_keys.contains(key)) {
		SQL_PREPARE(q, "UPDATE settings SET value=? WHERE key_=?");
	} else {
		SQL_PREPARE(q, "INSERT INTO settings (value, key_) VALUES (?,?)");
		db_keys << key;
	}
	q.bindValue(0, value);
	q.bindValue(1, key);
	q.exec();
	setAction(key, value);
	TransCommit();
}
