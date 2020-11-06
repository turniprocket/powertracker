import unittest
from app import create_app, db
from app.models import User, Group, Candidate, Party, Contributor, Contribution, Office, ContributionSource, Treasurer
from config import Config

class TestConfig(Config):
    TESTING=True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class UserModelCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def testing_groups(self):
        u1 = User(username='susan', email='susan@example.com')
        u2 = User(username='john', email='john@example.com')
        g1 = Group(group_name='admin')
        g2 = Group(group_name='editor')
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(g1)
        db.session.add(g2)
        db.session.commit()
        self.assertEqual(u1.groups.all(), [])
        self.assertEqual(u2.groups.all(), [])

        u1.add_to_group(g1)
        u1.add_to_group(g2)
        db.session.commit()
        self.assertTrue(u1.in_group(g1))
        self.assertTrue(u1.in_group(g2))

        u1.remove_from_group(g1)
        u1.remove_from_group(g2)
        db.session.commit()
        self.assertFalse(u1.in_group(g1))
        self.assertFalse(u1.in_group(g2))

    def testing_contributions(self):
        c1 = Candidate(first_name='bob', active=True)
        ct1 = Contributor(first_name='john')
        con1 = Contribution(amount=500)
        source1 = ContributionSource(title='Finance report 1')

        db.session.add(c1)
        db.session.add(ct1)
        db.session.add(con1)
        db.session.add(source1)
        db.session.commit()

        con1.set_candidate(c1)
        con1.set_contributor(ct1)
        con1.set_contribution_source(source1)
        db.session.commit()

        self.assertEqual(con1.get_candidate(), c1)
        self.assertEqual(con1.get_contributor(), ct1)
        self.assertEqual(con1.get_contribution_source(), source1)
        self.assertEqual(con1.amount, 500)

    def testing_candidates(self):
        c1 = Candidate(first_name='bob', active=True)
        p1 = Party(party_name='democratic')
        ct1 = Contributor(first_name='john')
        con1 = Contribution(amount=500)
        off1 = Office(office_name='Senator')
        off2 = Office(office_name='President')
        tres1 = Treasurer(first_name='george')

        db.session.add(c1)
        db.session.add(p1)
        db.session.add(ct1)
        db.session.add(con1)
        db.session.add(off1)
        db.session.add(off2)
        db.session.add(tres1)
        db.session.commit()

        self.assertTrue(c1.active)
        self.assertFalse(c1.get_party())
        self.assertFalse(c1.get_office_held())
        self.assertFalse(c1.get_office_sought())
        self.assertFalse(c1.get_treasurer())
        self.assertEqual(c1.get_received_contributions(), [])

        p1.add_candidate_member(c1)
        c1.set_office_held(off1)
        c1.set_office_sought(off2)
        c1.set_treasurer(tres1)
        con1.set_candidate(c1)
        con1.set_contributor(ct1)
        db.session.commit()

        self.assertEqual(c1.get_party(), p1)
        self.assertEqual(c1.get_office_held(), off1)
        self.assertEqual(c1.get_office_sought(), off2)
        self.assertEqual(c1.get_treasurer(), tres1)

        contribution = c1.get_received_contributions()
        self.assertEqual(500, contribution[0].amount)
        self.assertEqual(ct1, contribution[0].get_contributor())

    def testing_contributors(self):
        c1 = Candidate(first_name='bob')
        p1 = Party(party_name='democratic')
        ct1 = Contributor(first_name='john')
        con1 = Contribution(amount=500)

        db.session.add(c1)
        db.session.add(p1)
        db.session.add(ct1)
        db.session.add(con1)
        db.session.commit()

        self.assertFalse(ct1.get_party())
        self.assertEqual(ct1.get_contributions(), [])
        
        p1.add_candidate_member(c1)
        p1.add_contributor_member(ct1)
        con1.set_candidate(c1)
        con1.set_contributor(ct1)

        self.assertEqual(ct1.get_party(), p1)

        contributions = ct1.get_contributions()
        self.assertEqual(500, contributions[0].amount)
        self.assertEqual(ct1, contributions[0].get_contributor())

    def testing_parties(self):
        c1 = Candidate(first_name='bob', active=True)
        p1 = Party(party_name='democratic')
        ct1 = Contributor(first_name='john')

        db.session.add(c1)
        db.session.add(p1)
        db.session.add(ct1)
        db.session.commit()

        self.assertFalse(p1.candidate_in_party(c1))
        self.assertFalse(p1.contributor_in_party(ct1))

        p1.add_candidate_member(c1)
        p1.add_contributor_member(ct1)
        db.session.commit()

        self.assertTrue(p1.candidate_in_party(c1))
        self.assertTrue(p1.contributor_in_party(ct1))
        
        candidates = p1.get_candidates()
        contributors = p1.get_contributors()

        self.assertEqual(c1, candidates[0])
        self.assertEqual(ct1, contributors[0])

        p1.remove_candidate_member(c1)
        p1.remove_contributor_member(ct1)
        db.session.commit()

        self.assertFalse(p1.candidate_in_party(c1))
        self.assertFalse(p1.contributor_in_party(ct1))
        self.assertEqual(p1.candidate_members.all(), [])

    def testing_offices(self):
        c1 = Candidate(first_name='bob', active=True)
        off1 = Office(office_name='Senator')
        off2 = Office(office_name='President')

        db.session.add(c1)
        db.session.add(off1)
        db.session.add(off2)
        db.session.commit()

        self.assertFalse(off1.get_office_holder())

        c1.set_office_held(off1)
        c1.set_office_sought(off2)
        db.session.commit()

        seekers = off2.get_office_seekers()

        self.assertEqual(off1.get_office_holder(), c1)
        self.assertEqual(c1, seekers[0])

if __name__ == '__main__':
    unittest.main(verbosity=2)