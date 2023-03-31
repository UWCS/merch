from __script_setup import *

level = sys.argv[2].lower()
if level == "open":
    level = Visibility.OPEN
elif level == "closed":
    level = Visibility.CLOSED
elif level == "hidden":
    level = Visibility.HIDDEN
else:
    print("Level must be one of `open`, `closed` or `hidden`.")

with app.app_context():
    shop = db.session.query(Shop).first()
    item = (
        db.session.query(Item)
        .filter(Item.shop_id == shop.id)
        .filter(Item.name == sys.argv[1])
        .first()
    )
    print(item)
    item.visibility = level
    print(item)
    db.session.commit()
