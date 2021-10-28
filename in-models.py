from models import Session, family, costs, profits

session = Session()

MEMBER_1 = family(id=1, firstname='John', lastname='Smith', role='Father', age=40)

MEMBER_2 = family(id=2, firstname='Katherine', lastname='Smith', role='Mother', age=35)

MEMBER_3 = family(id=3, firstname='Andrew', lastname='Smith', role='Son', age=10)


COST_1 = costs(id=1, familyMemId=1, purpose='Car repair', amount=300)

COST_2 = costs(id=2, familyMemId=2, purpose='New phone', amount=500)

COST_3 = costs(id=3, familyMemId=3, purpose='Book', amount=20)

PROFIT_1 = profits(id=1, familyMemId=1, amount=3400)

PROFIT_2 = profits(id=2, familyMemId=2, amount=1500)

PROFIT_3 = profits(id=3, familyMemId=3, amount=50)

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