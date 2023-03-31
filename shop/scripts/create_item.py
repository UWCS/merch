from __script_setup import *

with app.app_context():
    shop = db.session.query(Shop).first()
    name = input("Name >>")
    url = input("Page URL >>")
    print(
        "Enter/Paste Description, can be multiline. Ctrl-D or Ctrl-Z (Windows) to continue"
    )
    contents = []
    while True:
        try:
            line = input(">>")
        except EOFError:
            break
        contents.append(line)
    description = "\n".join(contents)

    print("Enter image urls as indiviual lines. Ctrl-D or Ctrl-Z (Windows) to continue")
    images = []
    while True:
        try:
            line = input(">>")
        except EOFError:
            break
        images.append(line)

    item = Item(name=name, url=url, description=description, shop=shop)
    db.session.add(item)
    db.session.flush()

    for i, image in enumerate(images):
        if not image:
            continue
        db.session.add(Image(url=image, item_id=item.id, priority=i))
    db.session.commit()
