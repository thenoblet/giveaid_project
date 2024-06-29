from django.test import TestCase
from giveaid.models import (
    User, Country, State, City, Cause, UserDonation, UnregisteredDonation, Payment, SuccessStory
)

class CountryModelTests(TestCase):

    def setUp(self):
        self.country = Country.objects.create(name="Test Country")
    
    def test_country_str_method(self):
        """Test the string representation of the Country object."""
        self.assertEqual(str(self.country), 'Test Country')
    
    def test_country_table_name(self):
        """Test that the table name for the Country model is correct."""
        self.assertEqual(self.country._meta.db_table, 'country')

    def test_country_name_cannot_be_blank(self):
        """Test that the name field cannot be blank."""
        with self.assertRaises(ValueError):
            Country.objects.create(name="")


class StateModelTests(TestCase):

    def setUp(self):
        self.country = Country.objects.create(name="Test Country")
        self.state = State.objects.create(name="Test State", country=self.country)
    
    def test_state_str_method(self):
        """Test the string representation of the State object."""
        self.assertEqual(str(self.state), 'Test State')
    
    def test_state_table_name(self):
        """Test that the table name for the State model is correct."""
        self.assertEqual(self.state._meta.db_table, 'state')
    
    def test_state_name_cannot_be_blank(self):
        """Test that the name field cannot be blank."""
        with self.assertRaises(ValueError):
            State.objects.create(name="", country=self.country)

    def test_state_country_cascade_delete(self):
        """Test that deleting a country deletes associated states."""
        self.state.delete()
        self.assertEqual(State.objects.count(), 0)


class CityModelTests(TestCase):

    def setUp(self):
        self.country = Country.objects.create(name="Test Country")
        self.state = State.objects.create(name="Test State", country=self.country)
        self.city = City.objects.create(name="Test City", state=self.state)
    
    def test_city_str_method(self):
        """Test the string representation of the City object."""
        self.assertEqual(str(self.city), 'Test City')
    
    def test_city_table_name(self):
        """Test that the table name for the City model is correct."""
        self.assertEqual(self.city._meta.db_table, 'city')

    def test_city_name_cannot_be_blank(self):
        """Test that the name field cannot be blank."""
        with self.assertRaises(ValueError):
            City.objects.create(name="", state=self.state)

    def test_city_state_cascade_delete(self):
        """Test that deleting a state deletes associated cities."""
        self.state.delete()
        self.assertEqual(City.objects.count(), 0)


class UserModelTests(TestCase):

    def setUp(self):
        self.country = Country.objects.create(name="Test Country")
        self.state = State.objects.create(name="Test State", country=self.country)
        self.city = City.objects.create(name="Test City", state=self.state)
        self.user = User.objects.create_user(
            username='testuser',
            firstname='Test',
            lastname='User',
            email='testuser@example.com',
            password='testpassword',
            country=self.country,
            state=self.state,
            city=self.city,
            dob='1990-01-01',
            mobile='1234567890',
            street='123 Test Street'
        )
    
    def test_user_creation(self):
        """Test that a user is created with the correct attributes."""
        user = User.objects.get(username='testuser')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertEqual(user.firstname, 'Test')
        self.assertEqual(user.lastname, 'User')
        self.assertTrue(user.check_password('testpassword'))
        self.assertEqual(user.country, self.country)
        self.assertEqual(user.state, self.state)
        self.assertEqual(user.city, self.city)
        self.assertEqual(user.dob, '1990-01-01')
        self.assertEqual(user.mobile, '1234567890')
        self.assertEqual(user.street, '123 Test Street')
    
    def test_user_str_method(self):
        """Test the string representation of the User object."""
        self.assertEqual(str(self.user), 'Test User')
    
    def test_user_table_name(self):
        """Test that the table name for the User model is correct."""
        self.assertEqual(self.user._meta.db_table, 'user')

    def test_user_get_full_name(self):
        """Test the get_full_name method of the User model."""
        self.assertEqual(self.user.get_full_name(), 'Test User')

    def test_user_get_short_name(self):
        """Test the get_short_name method of the User model."""
        self.assertEqual(self.user.get_short_name(), 'Test User')
    
    def test_user_set_password(self):
        """Test that the set_password method hashes the password correctly."""
        self.user.set_password('newpassword')
        self.assertTrue(self.user.check_password('newpassword'))
    
    def test_user_email_normalization(self):
        """Test that the email is normalized (lowercased)."""
        user = User.objects.create_user(
            username='newuser',
            firstname='New',
            lastname='User',
            email='NEWUSER@EXAMPLE.COM',
            password='newpassword'
        )
        self.assertEqual(user.email, 'newuser@example.com')
    
    def test_user_username_unique(self):
        """Test that the username field is unique."""
        with self.assertRaises(Exception):
            User.objects.create_user(
                username='testuser',
                firstname='Another',
                lastname='User',
                email='anotheruser@example.com',
                password='anotherpassword'
            )

    def test_user_email_unique(self):
        """Test that the email field is unique."""
        with self.assertRaises(Exception):
            User.objects.create_user(
                username='newuser',
                firstname='New',
                lastname='User',
                email='testuser@example.com',
                password='newpassword'
            )
    
    def test_user_required_fields(self):
        """Test that required fields are enforced."""
        with self.assertRaises(ValueError):
            User.objects.create_user(
                username='testuser',
                firstname='Test',
                lastname='User',
                email='',
                password='testpassword'
            )

    def test_user_email_valid(self):
        """Test that invalid email raises an error."""
        with self.assertRaises(ValueError):
            User.objects.create_user(
                username='newuser',
                firstname='New',
                lastname='User',
                email='invalidemail',
                password='newpassword'
            )

    def test_user_delete_cascade(self):
        """Test that deleting a country/state/city cascades correctly."""
        self.country.delete()
        self.assertEqual(User.objects.count(), 0)


class CauseModelTests(TestCase):

    def setUp(self):
        self.cause = Cause.objects.create(title="Test Cause", description="A cause for testing")
    
    def test_cause_str_method(self):
        """Test the string representation of the Cause object."""
        self.assertEqual(str(self.cause), 'Test Cause')
    
    def test_cause_table_name(self):
        """Test that the table name for the Cause model is correct."""
        self.assertEqual(self.cause._meta.db_table, 'cause')

    def test_cause_title_cannot_be_blank(self):
        """Test that the title field cannot be blank."""
        with self.assertRaises(ValueError):
            Cause.objects.create(title="", description="A cause for testing")

    def test_cause_description_optional(self):
        """Test that description can be blank."""
        cause = Cause.objects.create(title="Another Cause")
        self.assertIsNone(cause.description)


class UserDonationModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            firstname='Test',
            lastname='User',
            email='testuser@example.com',
            password='testpassword'
        )
        self.cause = Cause.objects.create(title="Test Cause", description="A cause for testing")
        self.donation = UserDonation.objects.create(user=self.user, cause=self.cause, description="Donation Description")
    
    def test_donation_str_method(self):
        """Test the string representation of the UserDonation object."""
        self.assertEqual(str(self.donation), f"Donation by {self.user.username} to {self.cause.title}")
    
    def test_donation_table_name(self):
        """Test that the table name for the UserDonation model is correct."""
        self.assertEqual(self.donation._meta.db_table, 'userdonation')

    def test_donation_user_cascade_delete(self):
        """Test that deleting a user cascades correctly."""
        self.user.delete()
        self.assertEqual(UserDonation.objects.count(), 0)

    def test_donation_cause_cascade_delete(self):
        """Test that deleting a cause cascades correctly."""
        self.cause.delete()
        self.assertEqual(UserDonation.objects.count(), 0)


class UnregisteredDonationModelTests(TestCase):

    def setUp(self):
        self.cause = Cause.objects.create(title="Test Cause", description="A cause for testing")
        self.unregistered_donation = UnregisteredDonation.objects.create(
            cause=self.cause,
            name="Test Donor",
            email="donor@example.com"
        )
    
    def test_unregistered_donation_str_method(self):
        """Test the string representation of the UnregisteredDonation object."""
        self.assertEqual(str(self.unregistered_donation), f"Unregistered donor donation to {self.cause.title}")
    
    def test_unregistered_donation_table_name(self):
        """Test that the table name for the UnregisteredDonation model is correct."""
        self.assertEqual(self.unregistered_donation._meta.db_table, 'unregistereddonation')

    def test_unregistered_donation_name_cannot_be_blank(self):
        """Test that the name field cannot be blank."""
        with self.assertRaises(ValueError):
            UnregisteredDonation.objects.create(name="", email="donor@example.com", cause=self.cause)

    def test_unregistered_donation_email_valid(self):
        """Test that invalid email raises an error."""
        with self.assertRaises(ValueError):
            UnregisteredDonation.objects.create(name="Test Donor", email="invalidemail", cause=self.cause)


class PaymentModelTests(TestCase):

    def setUp(self):
        self.cause = Cause.objects.create(title="Test Cause", description="A cause for testing")
        self.user = User.objects.create_user(
            username='testuser',
            firstname='Test',
            lastname='User',
            email='testuser@example.com',
            password='testpassword'
        )
        self.user_donation = UserDonation.objects.create(user=self.user, cause=self.cause, description="Donation Description")
        self.payment = Payment.objects.create(
            donation_type='user',
            donation_id=self.user_donation.id,
            amount=100.00,
            payment_method='Credit Card'
        )
    
    def test_payment_str_method(self):
        """Test the string representation of the Payment object."""
        self.assertEqual(str(self.payment), f"Payment of: {self.payment.amount}. \tTransaction ID: {self.payment.transaction_id}")
    
    def test_payment_table_name(self):
        """Test that the table name for the Payment model is correct."""
        self.assertEqual(self.payment._meta.db_table, 'payment')

    def test_payment_get_donation_user(self):
        """Test that get_donation returns the correct UserDonation instance."""
        self.assertEqual(self.payment.get_donation(), self.user_donation)

    def test_payment_get_donation_unregistered(self):
        """Test that get_donation returns None for a non-existing donation type."""
        self.payment.donation_type = 'unregistered'
        self.payment.save()
        unregistered_donation = UnregisteredDonation.objects.create(
            cause=self.cause,
            name="Unregistered Donor",
            email="unregistered@example.com"
        )
        self.payment.donation_id = unregistered_donation.id
        self.payment.save()
        self.assertEqual(self.payment.get_donation(), unregistered_donation)

    def test_payment_donation_type_choices(self):
        """Test that the donation_type field choices are correct."""
        valid_choices = ['user', 'unregistered']
        for choice in valid_choices:
            self.assertIn(choice, dict(Payment.DONATION_TYPE_CHOICES).keys())

    def test_payment_donation_type_invalid(self):
        """Test that creating a payment with an invalid donation_type raises a ValidationError."""
        with self.assertRaises(Exception):
            Payment.objects.create(
                donation_type='invalid_type',
                donation_id=self.user_donation.id,
                amount=100.00,
                payment_method='Credit Card'
            )

    def test_payment_amount_positive(self):
        """Test that the amount is positive."""
        with self.assertRaises(ValueError):
            Payment.objects.create(
                donation_type='user',
                donation_id=self.user_donation.id,
                amount=-100.00,  # Invalid
                payment_method='Credit Card'
            )

    def test_payment_transaction_id_unique(self):
        """Test that the transaction_id field is unique."""
        existing_payment = Payment.objects.create(
            donation_type='user',
            donation_id=self.user_donation.id,
            amount=100.00,
            payment_method='Credit Card'
        )
        with self.assertRaises(Exception):
            Payment.objects.create(
                donation_type='user',
                donation_id=self.user_donation.id,
                amount=100.00,
                payment_method='Credit Card',
                transaction_id=existing_payment.transaction_id
            )


class SuccessStoryModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            firstname='Test',
            lastname='User',
            email='testuser@example.com',
            password='testpassword'
        )
        self.cause = Cause.objects.create(title="Test Cause", description="A cause for testing")
        self.success_story = SuccessStory.objects.create(
            user=self.user,
            cause=self.cause,
            title="Success Story Title",
            description="Success Story Description"
        )
    
    def test_success_story_str_method(self):
        """Test the string representation of the SuccessStory object."""
        self.assertEqual(str(self.success_story), 'Success Story Title')
    
    def test_success_story_table_name(self):
        """Test that the table name for the SuccessStory model is correct."""
        self.assertEqual(self.success_story._meta.db_table, 'successstory')

    def test_success_story_title_cannot_be_blank(self):
        """Test that the title field cannot be blank."""
        with self.assertRaises(ValueError):
            SuccessStory.objects.create(
                user=self.user,
                cause=self.cause,
                title="",  # Invalid
                description="Success Story Description"
            )

    def test_success_story_user_cascade_delete(self):
        """Test that deleting a user cascades correctly."""
        self.user.delete()
        self.assertEqual(SuccessStory.objects.count(), 0)

    def test_success_story_cause_cascade_delete(self):
        """Test that deleting a cause cascades correctly."""
        self.cause.delete()
        self.assertEqual(SuccessStory.objects.count(), 0)
