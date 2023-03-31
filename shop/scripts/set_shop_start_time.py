import __utils
from __script_setup import *

with app.app_context():
    new_time = __utils.parse_time(sys.argv[1])
    shop = db.session.query(Shop).first()
    print("Old", shop.start_time)
    print("New", new_time)
    shop.start_time = new_time
    db.session.commit()
