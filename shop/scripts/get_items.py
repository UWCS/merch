from __script_setup import *

with app.app_context():
    for shop in db.session.query(Shop).all():
        print("\n", shop)
        for item in shop.items:
            print("\n\t", item)
            for img in item.images:
                print("\t\t", img)
