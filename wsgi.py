from wahlprogramme import create_app
from wahlprogramme.database import load_db

# load database
db = load_db("data/", txt=False)
app = create_app(db)
