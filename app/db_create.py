from models import *


db.drop_all()
db.create_all()

c1 = Cat("Hockey")
c2 = Cat("Football")
c3 = Cat("Baseball")
c4 = Cat("Rugby")
c5 = Cat("Tennis")
c6 = Cat("Golf")
c7 = Cat("Cricket")

i1 = Items("Hockey Stick",
           "Its made of wood,\
            curved at the end. \
            Rubber grip for better control", c1)
i2 = Items("Hockey Ball", "Usually white in color. Very hard.", c1)
i3 = Items("Ball", "1 Feet diameter. Made of synthetic rubber.", c2)
i4 = Items("Shoes", "Made of rubber.", c2)
i5 = Items("Baseball bat", "Weighs 400 grams. Made of wood.", c3)
i6 = Items("Baseball ball", "Usually white in color. Very hard.", c3)
i7 = Items("Rugby Ball", "Oval shaped. Made of synthetic rubber.", c4)
i8 = Items("Shoes", "Made of rubber.", c4)
i9 = Items("Tennis racket.", "Weighs 400 grams. Made of wood.", c5)
i10 = Items("Tennis Ball", "Usually yellowish/greenish in color.", c5)
i11 = Items("Golf Ball", "3 inches diameter. Very hard.", c6)
i12 = Items("Golf cart.", "Runs on electricity. Handles 300 Kgs.", c6)
i13 = Items(
    "Cricket Bad", "Its made of wood.Rubber grip for better control", c7)
i14 = Items("Cricket Ball", "Hard inside. Leather outside.", c7)
i15 = Items("Cricket Gloves", "Made of rubber. Very durable.", c7)
i16 = Items("Shoes", "Made of rubber.", c7)

db.session.add(c1)
db.session.add(c2)
db.session.add(c3)
db.session.add(c4)
db.session.add(c5)
db.session.add(c6)
db.session.add(c7)

db.session.add(i1)
db.session.add(i2)
db.session.add(i3)
db.session.add(i4)
db.session.add(i5)
db.session.add(i6)
db.session.add(i7)
db.session.add(i8)
db.session.add(i9)
db.session.add(i10)
db.session.add(i11)
db.session.add(i12)
db.session.add(i13)
db.session.add(i14)
db.session.add(i15)
db.session.add(i16)

db.session.commit()

# items_py=[()]
# for i in Items.query.all():
# 	items_py.append((i.id,i.Naming,i.Description))
