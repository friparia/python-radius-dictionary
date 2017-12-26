from pyrad.dictionary import Dictionary
import config
import sys
import MySQLdb
import os


def import_by_file(path):
    dictionary = Dictionary(dict=path)

    db = MySQLdb.connect(config.DB_HOST, config.DB_USERNAME, config.DB_PASSWORD, 'radius_dictionary')
    cursor = db.cursor()
    for (key, vendor) in  dictionary.vendors.backward.items():
        if key == 0:
            continue
        sql = "INSERT IGNORE INTO `vendor` (`id`, `name`) VALUES ('" + str(key) + "', '" + vendor + "')"
        cursor.execute(sql)

    attributes = dictionary.attributes
    for (name, attribute) in attributes.items():
        vendor = dictionary.vendors.GetForward(attribute.vendor)
        sql = "INSERT IGNORE INTO `attribute` (`name`, `vendor`, `code`, `encrypt`, `has_tag`, `type`) VALUES ('" + attribute.name + "', '" + str(vendor) + "', '" + str(attribute.code) + "', '" + str(attribute.encrypt) + "', '" + str(int(attribute.has_tag)) + "', '" + str(attribute.type) + "')"
        cursor.execute(sql)
        types = ['string','octets','ipaddr','date','integer','signed','short','ipv6addr','ipv6prefix','ifid','integer64','abinary']
        if attribute.type not in types:
            print attribute.vendor, attribute.type
        if len(attribute.values):
            for (value_name, value) in attribute.values.forward.items():
                sql = "INSERT IGNORE INTO `value` (`vendor`, `code`, `name`, `value`)  VALUES ('" + str(vendor) + "', '" + str(attribute.code) + "', '" + value_name + "', UNHEX('" + value.encode('hex') + "'))"
    db.commit()


if __name__ == '__main__':
    path = sys.argv[1]
    if os.path.isfile(path):
        import_by_file(path)
    else:
        for file in os.listdir(path):
            print file
            import_by_file(path + '/' + file)
