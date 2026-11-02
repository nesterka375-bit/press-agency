import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from .forms import NewsForm, ContactForm
from .models import Newspaper, Topic


class TopicModelTests(TestCase):
    def test_str_returns_name(self):
        topic = Topic.objects.create(name="Politics")
        self.assertEqual(str(topic), "Politics")

    def test_ordering_by_name(self):
        Topic.objects.create(name="Sport")
        Topic.objects.create(name="Art")
        Topic.objects.create(name="Politics")
        names = list(Topic.objects.values_list("name", flat=True))
        self.assertEqual(names, ["Art", "Politics", "Sport"])


class RedactorModelTests(TestCase):
    def setUp(self):
        self.redactor = get_user_model().objects.create_user(
            username="john_doe",
            password="test12345",
            first_name="John",
            last_name="Doe",
            years_of_experience=5,
        )

    def test_str(self):
        self.assertEqual(
            str(self.redactor),
            "John Doe. Years of Experience: 5",
        )

    def test_years_of_experience_default_is_zero(self):
        user = get_user_model().objects.create_user(
            username="newbie", password="test12345"
        )
        self.assertEqual(user.years_of_experience, 0)

    def test_years_of_experience_can_be_null(self):
        user = get_user_model().objects.create_user(
            username="nullable",
            password="test12345",
            years_of_experience=None,
        )
        user.refresh_from_db()
        self.assertIsNone(user.years_of_experience)

    def test_create_user_with_years_of_experience(self):
        self.assertEqual(self.redactor.years_of_experience, 5)
        self.assertEqual(self.redactor.username, "john_doe")

    def test_password_is_hashed(self):
        self.assertNotEqual(self.redactor.password, "test12345")
        self.assertTrue(self.redactor.check_password("test12345"))

    def test_ordering_by_first_name(self):
        get_user_model().objects.create_user(
            username="alice", password="test12345", first_name="Alice"
        )
        get_user_model().objects.create_user(
            username="zed", password="test12345", first_name="Zed"
        )

        first_names = list(
            get_user_model().objects.values_list("first_name", flat=True)
        )

        self.assertEqual(first_names, sorted(first_names))


class NewspaperModelTests(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(name="Politics")
        self.redactor1 = get_user_model().objects.create_user(
            username="user1", password="test12345", first_name="Anna"
        )
        self.redactor2 = get_user_model().objects.create_user(
            username="user2", password="test12345", first_name="Boris"
        )
        self.newspaper = Newspaper.objects.create(
            title="Daily News",
            content="Some content",
            topic=self.topic,
        )

    def test_str(self):
        expected = (
            f"Daily News. Topic: Politics. " f"Date: {self.newspaper.published_date}"
        )
        self.assertEqual(str(self.newspaper), expected)

    def test_published_date_is_set_automatically(self):
        self.assertEqual(self.newspaper.published_date, datetime.date.today())

    def test_published_date_not_changed_on_update(self):
        original_date = self.newspaper.published_date
        self.newspaper.title = "Updated title"
        self.newspaper.save()
        self.newspaper.refresh_from_db()
        self.assertEqual(self.newspaper.published_date, original_date)

    def test_topic_relation(self):
        self.assertEqual(self.newspaper.topic, self.topic)
        self.assertIn(self.newspaper, self.topic.newspapers.all())

    def test_delete_topic_cascades_to_newspapers(self):
        self.topic.delete()
        self.assertEqual(Newspaper.objects.count(), 0)

    def test_publishers_can_be_empty(self):
        self.assertEqual(self.newspaper.publishers.count(), 0)

    def test_add_multiple_publishers(self):
        self.newspaper.publishers.add(self.redactor1, self.redactor2)
        self.assertEqual(self.newspaper.publishers.count(), 2)
        self.assertIn(self.redactor1, self.newspaper.publishers.all())
        self.assertIn(self.redactor2, self.newspaper.publishers.all())

    def test_redactor_related_name_newspapers(self):
        self.newspaper.publishers.add(self.redactor1)
        self.assertIn(self.newspaper, self.redactor1.newspapers.all())
        self.assertEqual(self.redactor2.newspapers.count(), 0)

    def test_delete_redactor_does_not_delete_newspaper(self):
        self.newspaper.publishers.add(self.redactor1)
        self.redactor1.delete()
        self.assertTrue(Newspaper.objects.filter(pk=self.newspaper.pk).exists())
        self.assertEqual(self.newspaper.publishers.count(), 0)

    def test_ordering_by_title_for_same_date(self):
        Newspaper.objects.create(title="Alpha", content="c", topic=self.topic)
        Newspaper.objects.create(title="Zeta", content="c", topic=self.topic)
        titles = list(Newspaper.objects.values_list("title", flat=True))
        self.assertEqual(titles, ["Alpha", "Daily News", "Zeta"])

    def test_ordering_by_published_date_descending(self):
        old = Newspaper.objects.create(title="Old", content="c", topic=self.topic)
        Newspaper.objects.filter(pk=old.pk).update(
            published_date=datetime.date(2020, 1, 1)
        )
        newspapers = list(Newspaper.objects.all())
        self.assertEqual(newspapers[-1], old)


class NewsFormTests(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(name="Politics")
        self.redactor1 = get_user_model().objects.create_user(
            username="user1", password="test12345"
        )
        self.redactor2 = get_user_model().objects.create_user(
            username="user2", password="test12345"
        )
        self.valid_data = {
            "title": "Daily News",
            "content": "Some content",
            "topic": self.topic.pk,
            "publishers": [self.redactor1.pk, self.redactor2.pk],
        }

    def test_form_fields(self):
        form = NewsForm()
        self.assertEqual(list(form.fields), ["title", "content", "topic", "publishers"])

    def test_valid_form(self):
        form = NewsForm(data=self.valid_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_publishers_are_optional(self):
        data = {**self.valid_data, "publishers": []}
        form = NewsForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_title_required(self):
        data = {**self.valid_data, "title": ""}
        form = NewsForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_content_required(self):
        data = {**self.valid_data, "content": ""}
        form = NewsForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("content", form.errors)

    def test_topic_required(self):
        data = {**self.valid_data}
        data.pop("topic")
        form = NewsForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("topic", form.errors)

    def test_invalid_topic(self):
        data = {**self.valid_data, "topic": 9999}
        form = NewsForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("topic", form.errors)

    def test_invalid_publisher(self):
        data = {**self.valid_data, "publishers": [9999]}
        form = NewsForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("publishers", form.errors)

    def test_title_too_long(self):
        data = {**self.valid_data, "title": "a" * 256}
        form = NewsForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_save_creates_newspaper_with_publishers(self):
        form = NewsForm(data=self.valid_data)
        self.assertTrue(form.is_valid(), form.errors)
        newspaper = form.save()
        self.assertEqual(Newspaper.objects.count(), 1)
        self.assertEqual(newspaper.title, "Daily News")
        self.assertEqual(newspaper.topic, self.topic)
        self.assertEqual(newspaper.publishers.count(), 2)

    def test_widgets_css_classes(self):
        form = NewsForm()
        self.assertEqual(form.fields["title"].widget.attrs["class"], "form-control")
        self.assertEqual(form.fields["content"].widget.attrs["class"], "form-control")
        self.assertEqual(form.fields["topic"].widget.attrs["class"], "form-select")
        self.assertEqual(form.fields["publishers"].widget.attrs["class"], "form-select")

    def test_widget_attributes(self):
        form = NewsForm()
        self.assertEqual(
            form.fields["title"].widget.attrs["placeholder"], "Enter title"
        )
        self.assertEqual(form.fields["content"].widget.attrs["rows"], 5)
        self.assertEqual(form.fields["publishers"].widget.attrs["size"], 4)


class ContactFormTests(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "message": "Hello, this is a test message.",
        }

    def test_valid_form(self):
        form = ContactForm(data=self.valid_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_cleaned_data(self):
        form = ContactForm(data=self.valid_data)
        form.is_valid()
        self.assertEqual(form.cleaned_data["name"], "John Doe")
        self.assertEqual(form.cleaned_data["email"], "john@example.com")
        self.assertEqual(form.cleaned_data["message"], "Hello, this is a test message.")

    def test_empty_form_is_invalid(self):
        form = ContactForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(set(form.errors), {"name", "email", "message"})

    def test_name_required(self):
        data = {**self.valid_data, "name": ""}
        form = ContactForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_name_max_length(self):
        data = {**self.valid_data, "name": "a" * 101}
        form = ContactForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_name_at_max_length_is_valid(self):
        data = {**self.valid_data, "name": "a" * 100}
        form = ContactForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_email_required(self):
        data = {**self.valid_data, "email": ""}
        form = ContactForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_invalid_email(self):
        for bad_email in ["plainaddress", "john@", "@example.com", "john@@example.com"]:
            with self.subTest(email=bad_email):
                data = {**self.valid_data, "email": bad_email}
                form = ContactForm(data=data)
                self.assertFalse(form.is_valid())
                self.assertIn("email", form.errors)

    def test_message_required(self):
        data = {**self.valid_data, "message": ""}
        form = ContactForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("message", form.errors)

    def test_whitespace_only_message_is_invalid(self):
        data = {**self.valid_data, "message": "   "}
        form = ContactForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("message", form.errors)

    def test_widget_ids_and_classes(self):
        form = ContactForm()
        for field in ("name", "email", "message"):
            with self.subTest(field=field):
                attrs = form.fields[field].widget.attrs
                self.assertEqual(attrs["class"], "form-control")
                self.assertEqual(attrs["id"], field)
