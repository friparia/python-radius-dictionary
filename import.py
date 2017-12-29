import config
import sys
import MySQLdb
import os
import struct
from dictionary import Dictionary


def import_by_file(path):
    dictionary = Dictionary(dict=path)

    db = MySQLdb.connect(config.DB_HOST, config.DB_USERNAME, config.DB_PASSWORD, 'radius_dictionary')
    cursor = db.cursor()
    for (key, vendor) in  dictionary.vendors.backward.items():
        if key == 0:
            continue
        t,l = dictionary.vendor_formats[key]
        sql = "INSERT IGNORE INTO `rad_vendor` (`id`, `name`, `type_length`, `length_length`) VALUES ('" + str(key) + "', '" + vendor + "', " + str(t) + ", " + str(l) + ")"
        cursor.execute(sql)

    attributes = dictionary.attributes
    for (name, attribute) in attributes.items():
        vendor = dictionary.vendors.GetForward(attribute.vendor)
        sql = "INSERT IGNORE INTO `rad_attribute` (`name`, `vendor`, `code`, `encrypt`, `has_tag`, `type`) VALUES ('" + attribute.name + "', '" + str(vendor) + "', '" + str(attribute.code) + "', '" + str(attribute.encrypt) + "', '" + str(int(attribute.has_tag)) + "', '" + str(attribute.type) + "')"
        cursor.execute(sql)
        if len(attribute.values):
            for (value_name, value) in attribute.values.forward.items():
                sql = "INSERT IGNORE INTO `rad_value` (`vendor`, `code`, `name`, `value`)  VALUES ('" + str(vendor) + "', '" + str(attribute.code) + "', '" + value_name + "', " +  value + ")"
                cursor.execute(sql)
    #db.commit()


if __name__ == '__main__':
    path = sys.argv[1]
    if os.path.isfile(path):
        import_by_file(path)
    else:
        for file in os.listdir(path):
            print file
            import_by_file(path + '/' + file)
