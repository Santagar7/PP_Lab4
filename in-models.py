from models import *

session = Session()

FAMILY_1 = family(name='Smiths')

MEMBER_1 = family_members(familyId=1, firstname='John', lastname='Smith', role='Father', age=40)

MEMBER_2 = family_members(familyId=1, firstname='Katherine', lastname='Smith', role='Mother', age=35)

MEMBER_3 = family_members(familyId=1, firstname='Andrew', lastname='Smith', role='Son', age=10)

COST_1 = costs(familyMemId=1, purpose='Car repair', amount=300)

COST_2 = costs(familyMemId=2, purpose='New phone', amount=500)

COST_3 = costs(familyMemId=3, purpose='Book', amount=20)

PROFIT_1 = profits(familyMemId=1, amount=3400)

PROFIT_2 = profits(familyMemId=2, amount=1500)

PROFIT_3 = profits(familyMemId=3, amount=50)


session.add(FAMILY_1)
session.commit()
session.add(MEMBER_1)
session.add(MEMBER_2)
session.add(MEMBER_3)
session.commit()
session.add(COST_1)
session.add(COST_2)
session.add(COST_3)
session.add(PROFIT_1)
session.add(PROFIT_2)
session.add(PROFIT_3)
session.commit()

print(session.query(family).all()[0])
print(session.query(profits).all()[1])
print(session.query(costs).all())

session.close()