from __script_setup import *

with app.app_context():
    db.session.add(shop := Shop(name=sys.argv[1], visibility=Visibility.HIDDEN))
    print(shop)
    db.session.commit()
