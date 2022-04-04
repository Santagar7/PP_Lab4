import unittest
from base64 import b64encode
from sqlalchemy.orm import sessionmaker
from API.fl_app import app
from API.utils import bcrypt
import json

from API.models_api import FamilyMembers, engine, Family, Costs, Profits

Session = sessionmaker(bind=engine)


class TestingBase(unittest.TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    app_context = app.app_context()
    app_context.push()
    tester = app.test_client()
    session = Session()

    def tearDown(self):
        self.session.query(FamilyMembers).filter_by(login='ANDREAS').delete()
        self.session.commit()
        self.close_session()

    def close_session(self):
        self.session.close()


class ApiTest(TestingBase):
    family = {
        "name": "Andreas"
    }

    member = {
        "login": 'ANDREAS',
        "password": '99999999',
        "familyId": 1,
        "firstname": 'Andreas',
        "lastname": 'Andreas',
        "role": 'Man',
        "birthdate": '1977-10-23'
    }

    cost = {
        "purpose": 'Car repair',
        "amount": 300
    }

    profit = {
        "amount": 300
    }

    def test_member_creation_success(self):
        response = self.tester.post("/family_members", data=json.dumps(self.member),
                                    content_type="application/json")

        code = response.status_code
        self.assertEqual(200, code)
        self.session.query(FamilyMembers).filter_by(login='ANDREAS').delete()
        self.session.commit()

    def test_member_creation_invalid(self):
        response = self.tester.post("/family_members", data=json.dumps({
            "familyId": 2,
            "login": 'john1977',
            "password": '99999999',
            "firstname": 'Andreas',
            "lastname": 'Andreas',
            "role": 'Man',
            "birthdate": '1977-10-23'
        }), content_type="application/json")
        code = response.status_code
        self.assertEqual(400, code)

    def test_member_alter_success(self):
        hashpassword = bcrypt.generate_password_hash('99999999')
        member = FamilyMembers(login="ANDREAS", firstname="Andreas", lastname="Andreas", role='Father',
                               birthdate='1977-05-10', password=hashpassword, familyId=1)
        self.session.add(member)
        self.session.commit()
        creds = b64encode(b"ANDREAS:99999999").decode("utf-8")
        response = self.tester.put('/family_members',
                                   data=json.dumps(
                                       {"login": 'ANDREAS',
                                        "password": '99999999',
                                        "familyId": 2,
                                        "firstname": 'ASASASA',
                                        "lastname": 'Andreas',
                                        "role": 'Man',
                                        "birthdate": '1977-10-23'}),
                                   content_type='application/json', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(200, code)
        self.session.query(FamilyMembers).filter_by(login='ANDREAS').delete()
        self.session.commit()

    def test_delete_member(self):
        hashpassword = bcrypt.generate_password_hash('99999999')
        member = FamilyMembers(login="ANDREAS", firstname="Andreas", lastname="Andreas", role='Father',
                               birthdate='1977-05-10', password=hashpassword, familyId=1)
        self.session.add(member)
        self.session.commit()
        creds = b64encode(b"ANDREAS:99999999").decode("utf-8")
        response = self.tester.delete('/family_members', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(200, code)

    def test_get_members(self):
        response = self.tester.get('/family_members')
        code = response.status_code
        self.assertEqual(200, code)

    def test_family_create(self):
        response = self.tester.post("/family", data=json.dumps(self.family),
                                    content_type="application/json")
        code = response.status_code
        self.assertEqual(200, code)
        self.session.query(Family).filter_by(id=3).delete()
        self.session.commit()

    def test_family_alter(self):
        hashpassword = bcrypt.generate_password_hash('99999999')
        family = Family(id=5, name='ksjdjbfsd')
        member = FamilyMembers(login="ANDREAS", firstname="Andreas", lastname="Andreas", role='Father',
                               birthdate='1977-05-10', password=hashpassword, familyId=5)
        self.session.add(member)
        self.session.add(family)
        self.session.commit()
        creds = b64encode(b"ANDREAS:99999999").decode("utf-8")
        response = self.tester.put('/family/5',
                                   data=json.dumps(
                                       {"name": "dlfnsdkjfn"}),
                                   content_type='application/json', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(200, code)
        self.session.query(FamilyMembers).filter_by(login='ANDREAS').delete()
        self.session.query(Family).filter_by(id=5).delete()
        self.session.commit()

    def test_cost_create(self):
        hashpassword = bcrypt.generate_password_hash('99999999')
        member = FamilyMembers(login="ANDREAS", firstname="Andreas", lastname="Andreas", role='Father',
                               birthdate='1977-05-10', password=hashpassword, familyId=1)
        self.session.add(member)
        self.session.commit()
        creds = b64encode(b"ANDREAS:99999999").decode("utf-8")
        response = self.tester.post("/costs", data=json.dumps(self.cost),
                                    content_type="application/json", headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(200, code)
        self.session.query(FamilyMembers).filter_by(login='ANDREAS').delete()
        self.session.query(Costs).filter_by(id=7).delete()
        self.session.commit()

    def test_cost_alter(self):
        hashpassword = bcrypt.generate_password_hash('99999999')
        member = FamilyMembers(id=14, login="ANDREAS", firstname="Andreas", lastname="Andreas", role='Father',
                               birthdate='1977-05-10', password=hashpassword, familyId=1)
        cost = Costs(familyMemId=14, familyId=1, purpose='Car repair', amount=300)
        self.session.add(member)
        self.session.commit()
        self.session.add(cost)
        self.session.commit()
        creds = b64encode(b"ANDREAS:99999999").decode("utf-8")
        response = self.tester.put('/costs/7',
                                   data=json.dumps(
                                       {
                                           "purpose": 'Car repair',
                                           "amount": 500}),
                                   content_type='application/json', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.session.query(FamilyMembers).filter_by(login='ANDREAS').delete()
        self.session.query(Costs).filter_by(id=7).delete()
        self.session.commit()
        self.assertEqual(200, code)

    def test_cost_delete(self):
        hashpassword = bcrypt.generate_password_hash('99999999')
        member = FamilyMembers(id=14, login="ANDREAS", firstname="Andreas", lastname="Andreas", role='Father',
                               birthdate='1977-05-10', password=hashpassword, familyId=1)
        cost = Costs(id=20, familyMemId=14, familyId=1, purpose='Car repair', amount=300)
        self.session.add(member)
        self.session.commit()
        self.session.add(cost)
        self.session.commit()
        creds = b64encode(b"ANDREAS:99999999").decode("utf-8")
        response = self.tester.delete('/costs/20', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(200, code)

    def test_cost_get(self):
        hashpassword = bcrypt.generate_password_hash('99999999')
        member = FamilyMembers(id=14, login="ANDREAS", firstname="Andreas", lastname="Andreas", role='Father',
                               birthdate='1977-05-10', password=hashpassword, familyId=1)
        cost = Costs(id=20, familyMemId=14, familyId=1, purpose='Car repair', amount=300)
        self.session.add(member)
        self.session.commit()
        self.session.add(cost)
        self.session.commit()
        creds = b64encode(b"ANDREAS:99999999").decode("utf-8")
        response = self.tester.get('/costs/member', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.session.query(Costs).filter_by(id=20).delete()
        self.session.query(FamilyMembers).filter_by(login='ANDREAS').delete()
        self.session.commit()
        self.assertEqual(200, code)

    def test_cost_get_id(self):
        hashpassword = bcrypt.generate_password_hash('99999999')
        member = FamilyMembers(id=14, login="ANDREAS", firstname="Andreas", lastname="Andreas", role='Father',
                               birthdate='1977-05-10', password=hashpassword, familyId=1)
        cost = Costs(id=20, familyMemId=14, familyId=1, purpose='Car repair', amount=300)
        self.session.add(member)
        self.session.commit()
        self.session.add(cost)
        self.session.commit()
        creds = b64encode(b"ANDREAS:99999999").decode("utf-8")
        response = self.tester.get('/costs/20', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.session.query(Costs).filter_by(id=20).delete()
        self.session.query(FamilyMembers).filter_by(login='ANDREAS').delete()
        self.session.commit()
        self.assertEqual(200, code)

    def test_cost_get_family(self):
        hashpassword = bcrypt.generate_password_hash('99999999')
        member = FamilyMembers(id=14, login="ANDREAS", firstname="Andreas", lastname="Andreas", role='Father',
                               birthdate='1977-05-10', password=hashpassword, familyId=1)
        cost = Costs(id=20, familyMemId=14, familyId=1, purpose='Car repair', amount=300)
        self.session.add(member)
        self.session.commit()
        self.session.add(cost)
        self.session.commit()
        creds = b64encode(b"ANDREAS:99999999").decode("utf-8")
        response = self.tester.get('/costs/family', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.session.query(Costs).filter_by(id=20).delete()
        self.session.query(FamilyMembers).filter_by(login='ANDREAS').delete()
        self.session.commit()
        self.assertEqual(200, code)

    def test_profit_create(self):
        hashpassword = bcrypt.generate_password_hash('99999999')
        member = FamilyMembers(login="ANDREAS", firstname="Andreas", lastname="Andreas", role='Father',
                               birthdate='1977-05-10', password=hashpassword, familyId=1)
        self.session.add(member)
        self.session.commit()
        creds = b64encode(b"ANDREAS:99999999").decode("utf-8")
        response = self.tester.post("/profits", data=json.dumps(self.profit),
                                    content_type="application/json", headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(200, code)
        self.session.query(FamilyMembers).filter_by(login='ANDREAS').delete()
        self.session.query(Profits).filter_by(id=7).delete()
        self.session.commit()

    def test_profit_alter(self):
        hashpassword = bcrypt.generate_password_hash('99999999')
        member = FamilyMembers(id=14, login="ANDREAS", firstname="Andreas", lastname="Andreas", role='Father',
                               birthdate='1977-05-10', password=hashpassword, familyId=1)
        profit = Profits(familyMemId=14, familyId=1, amount=300)
        self.session.add(member)
        self.session.commit()
        self.session.add(profit)
        self.session.commit()
        creds = b64encode(b"ANDREAS:99999999").decode("utf-8")
        response = self.tester.put('/profits/7',
                                   data=json.dumps(
                                       {
                                           "amount": 500}),
                                   content_type='application/json', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.session.query(FamilyMembers).filter_by(login='ANDREAS').delete()
        self.session.query(Profits).filter_by(id=7).delete()
        self.session.commit()
        self.assertEqual(200, code)

    def test_profit_delete(self):
        hashpassword = bcrypt.generate_password_hash('99999999')
        member = FamilyMembers(id=14, login="ANDREAS", firstname="Andreas", lastname="Andreas", role='Father',
                               birthdate='1977-05-10', password=hashpassword, familyId=1)
        profit = Profits(familyMemId=14, familyId=1, amount=300)
        self.session.add(member)
        self.session.commit()
        self.session.add(profit)
        self.session.commit()
        profit1 = self.session.query(Profits).filter_by(familyMemId=14).first()
        creds = b64encode(b"ANDREAS:99999999").decode("utf-8")
        response = self.tester.delete(f'/profits/{profit1.id}', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(200, code)

    def test_profit_get(self):
        hashpassword = bcrypt.generate_password_hash('99999999')
        member = FamilyMembers(id=14, login="ANDREAS", firstname="Andreas", lastname="Andreas", role='Father',
                               birthdate='1977-05-10', password=hashpassword, familyId=1)
        profit = Profits(id=20, familyMemId=14, familyId=1, amount=300)
        self.session.add(member)
        self.session.commit()
        self.session.add(profit)
        self.session.commit()
        creds = b64encode(b"ANDREAS:99999999").decode("utf-8")
        response = self.tester.get('/profits/member', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.session.query(Profits).filter_by(id=20).delete()
        self.session.query(FamilyMembers).filter_by(login='ANDREAS').delete()
        self.session.commit()
        self.assertEqual(200, code)

    def test_profit_get_id(self):
        hashpassword = bcrypt.generate_password_hash('99999999')
        member = FamilyMembers(id=14, login="ANDREAS", firstname="Andreas", lastname="Andreas", role='Father',
                               birthdate='1977-05-10', password=hashpassword, familyId=1)
        profit = Profits(familyMemId=14, familyId=1, amount=300)
        self.session.add(member)
        self.session.commit()
        self.session.add(profit)
        self.session.commit()
        creds = b64encode(b"ANDREAS:99999999").decode("utf-8")
        profit1 = self.session.query(Profits).filter_by(familyMemId=14).first()
        response = self.tester.get(f'/profits/{profit1.id}', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.session.query(Profits).filter_by(id=profit1.id).delete()
        self.session.query(FamilyMembers).filter_by(login='ANDREAS').delete()
        self.session.commit()
        self.assertEqual(200, code)

    def test_profit_get_family(self):
        hashpassword = bcrypt.generate_password_hash('99999999')
        member = FamilyMembers(id=14, login="ANDREAS", firstname="Andreas", lastname="Andreas", role='Father',
                               birthdate='1977-05-10', password=hashpassword, familyId=1)
        profit = Profits(id=20, familyMemId=14, familyId=1, amount=300)
        self.session.add(member)
        self.session.commit()
        self.session.add(profit)
        self.session.commit()
        creds = b64encode(b"ANDREAS:99999999").decode("utf-8")
        response = self.tester.get('/profits/family', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.session.query(Profits).filter_by(id=20).delete()
        self.session.query(FamilyMembers).filter_by(login='ANDREAS').delete()
        self.session.commit()
        self.assertEqual(200, code)


if __name__ == '__main__':
    unittest.main()
    app.run()
