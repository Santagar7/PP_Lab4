from API.models_api import *

FAMILY_1 = Family(name='Smiths')
FAMILY_2 = Family(name='Jonsons')

MEMBER_1 = FamilyMembers(familyId=1, login='john1977', password='11111111', firstname='John',
                         lastname='Smith', role='Father', birthdate='1977-05-10')
MEMBER_2 = FamilyMembers(familyId=1, login='kathrine2536', password='22222222', firstname='Katherine',
                         lastname='Smith', role='Mother', birthdate='1984-05-29')
MEMBER_3 = FamilyMembers(familyId=1, login='andrew8uq8', password='33333333', firstname='Andrew',
                         lastname='Smith', role='Son', birthdate='2008-12-12')
MEMBER_4 = FamilyMembers(familyId=2, login='maxjohnson23', password='44444444', firstname='Max',
                         lastname='Jonson', role='Father', birthdate='1981-05-04')
MEMBER_5 = FamilyMembers(familyId=2, login='mary2321', password='55555555', firstname='Mary',
                         lastname='Jonson', role='Mother', birthdate='1984-02-12')
MEMBER_6 = FamilyMembers(familyId=2, login='susie2315r', password='66666666', firstname='Susie',
                         lastname='Johnson', role='Daughter', birthdate='2005-10-23')

COST_1 = Costs(familyMemId=1, familyId=1, purpose='Car repair', amount=300)
COST_2 = Costs(familyMemId=2, familyId=1, purpose='New phone', amount=500)
COST_3 = Costs(familyMemId=3, familyId=1, purpose='Book', amount=20)
COST_4 = Costs(familyMemId=4, familyId=2, purpose='Laptop', amount=1000)
COST_5 = Costs(familyMemId=5, familyId=2, purpose='Jacket', amount=100)
COST_6 = Costs(familyMemId=6, familyId=2, purpose='Computer game', amount=60)

PROFIT_1 = Profits(familyMemId=1, familyId=1, amount=3400)
PROFIT_2 = Profits(familyMemId=2, familyId=1, amount=1500)
PROFIT_3 = Profits(familyMemId=3, familyId=1, amount=50)
PROFIT_4 = Profits(familyMemId=4, familyId=2, amount=4000)
PROFIT_5 = Profits(familyMemId=5, familyId=2, amount=2000)
PROFIT_6 = Profits(familyMemId=6, familyId=2, amount=100)


with Session() as session:
    session.add(FAMILY_1)
    session.add(FAMILY_2)
    session.commit()
    session.add(MEMBER_1)
    session.add(MEMBER_2)
    session.add(MEMBER_3)
    session.add(MEMBER_4)
    session.add(MEMBER_5)
    session.add(MEMBER_6)
    session.commit()
    session.add(COST_1)
    session.add(COST_2)
    session.add(COST_3)
    session.add(COST_4)
    session.add(COST_5)
    session.add(COST_6)
    session.add(PROFIT_1)
    session.add(PROFIT_2)
    session.add(PROFIT_3)
    session.add(PROFIT_4)
    session.add(PROFIT_5)
    session.add(PROFIT_6)
    session.commit()

print(session.query(Family).all()[0])
print(session.query(Profits).all()[1])
print(session.query(Costs).all())