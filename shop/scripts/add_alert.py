import __utils
from __script_setup import *

with app.app_context():
    start_time = __utils.parse_time(sys.argv[2])
    end_time = __utils.parse_time(sys.argv[3])
    title = sys.argv[4]
    if len(sys.argv) == 6:
        title, text = sys.argv[4], sys.argv[5]
    else:
        title, text = None, sys.argv[4]

    shop = db.session.query(Shop).first()
    db.session.add(
        alert := Alert(
            name=sys.argv[1],
            shop=shop,
            start_time=start_time,
            end_time=end_time,
            title=title,
            text=text,
        )
    )
    print(alert)
    db.session.commit()
