from core.models import (
    AOI,
    Dataset,
    Feedback,
    FeedbackAOI,
    FeedbackLabel,
    Label,
    Model,
    Training,
)
from django.contrib.gis.geos import Polygon
from django.test import TestCase
from login.models import OsmUser
from model_bakery import baker


class DatasetModelTest(TestCase):
    def setUp(self):
        # Create a Dataset instance for testing
        self.dataset = baker.make(Dataset, name="Test Dataset")

    def test_dataset_creation(self):
        # Test that the Dataset instance has been created properly.
        self.assertEqual(self.dataset.name, "Test Dataset")

    def test_invalid_dataset_creation(self):
        # Test thet the Dataset instance return an exception if missing needed values.
        with self.assertRaises(Exception):
            self.dataset = baker.make(created_by=None)

    def test_dataset_fields(self):
        # Test all fields for correct values
        self.assertEqual(self.dataset.name, "Test Dataset")
        # Ensure auto_now_add fields are populated
        self.assertIsNotNone(self.dataset.created_at)
        # Ensure auto_now fields are populated
        self.assertIsNotNone(self.dataset.last_modified)

    def test_dataset_string_representation(self):
        # Test the string representation of a Dataset instance
        self.assertEqual(str(self.dataset), "Test Dataset")


class AOIModelTest(TestCase):
    def setUp(self):
        # Create a Dataset instance for testing
        self.dataset = baker.make(Dataset, name="Test Dataset")
        # Create an AOI instance for testing
        self.aoi = baker.make(
            AOI,
            dataset=self.dataset,
            geom="POLYGON((0 0, 0 1, 1 1, 1 0, 0 0))",
            label_status=AOI.DownloadStatus.DOWNLOADED,
        )

    def test_aoi_creation(self):
        # Test that the AOI instance has been created properly.
        self.assertEqual(self.aoi.dataset, self.dataset)

    def test_invalid_aoi_creation(self):
        # Test that an invalid AOI instance creation returns an exception.
        with self.assertRaises(Exception):
            self.aoi = baker.make(AOI, dataset=None)

    def test_aoi_geom(self):
        # Test the geom field of the AOI instance.
        self.assertIsInstance(self.aoi.geom, Polygon)

    def test_aoi_label_default_status(self):
        # Test the default label_status field of the AOI instance is DOWNLOADED.
        self.assertEqual(self.aoi.label_status, AOI.DownloadStatus.DOWNLOADED)

    def test_aoi_label_fetched(self):
        # Test the label_fetched field of the AOI instance.
        self.assertIsNone(self.aoi.label_fetched)

    def test_aoi_created_at(self):
        # Test the created_at field of the AOI instance.
        self.assertIsNotNone(self.aoi.created_at)

    def test_aoi_last_modified(self):
        # Test the last_modified field of the AOI instance is not empty after creation.
        self.assertIsNotNone(self.aoi.last_modified)

    def test_aoi_string_representation(self):
        # Test the string representation of an AOI instance.
        self.assertEqual(str(self.aoi), f"Test Dataset - {self.aoi.geom}")


class LabelModelTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.osm_user = baker.make(OsmUser, osm_id="123456789", username="testuser")

        # Create a Dataset instance for testing
        self.dataset = baker.make(
            Dataset, name="Test Dataset", created_by=self.osm_user
        )

        # Create an AOI instance for testing
        self.aoi = baker.make(
            AOI, dataset=self.dataset, geom="POLYGON((0 0, 0 1, 1 1, 1 0, 0 0))"
        )

        # Create a Label instance for testing
        self.label = baker.make(
            Label,
            aoi=self.aoi,
            geom="POLYGON((0 0, 0 1, 1 1, 1 0, 0 0))",
            osm_id=123456789,
            tags={"key": "value"},
        )

    def test_label_creation(self):
        # Test the Label instance has been created properly.
        self.assertTrue(isinstance(self.label, Label))

    def test_string_representation(self):
        # Test the string representation of an Label instance
        self.assertEqual(
            str(self.label),
            f"{self.label.aoi} - {self.label.geom}",
        )

    def test_invalid_label_creation(self):
        # Raise an exception if an invalid label is created
        with self.assertRaises(Exception):
            self.label = baker.make(
                Label,
                aoi=None,
                geom="POLYGON((0 0, 0 1, 1 1, 1 0, 0 0))",
                osm_id=123456789,
                tags={"key": "value"},
            )

    def test_created_at_field(self):
        # Test the created_by field is not empty
        self.assertIsNotNone(self.label.created_at)


class ModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.osm_user = baker.make(OsmUser, osm_id="123456789", username="testuser")
        cls.dataset = baker.make(
            Dataset,
            name="Test Dataset",
            created_by=cls.osm_user,
            source_imagery="http://example.com/image.png",
        )
        cls.model = baker.make(
            Model, name="Test Model", created_by=cls.osm_user, dataset=cls.dataset
        )

    def test_model_creation(self):
        # Test the Model instance has been created properly.
        self.assertTrue(isinstance(self.model, Model))

    def test_invalid_model_creation(self):
        # Raise an exception if an invalid model is created
        with self.assertRaises(Exception):
            self.model = baker.make(
                Model, name="Test Model", created_by=None, dataset=self.dataset
            )

    def test_string_representation(self):
        # Test the string representation of a Model instance
        self.assertEqual(str(self.model), self.model.name)

    def test_created_by_field(self):
        # Test the created_by field is not empty
        self.assertIsNotNone(self.model.created_by)


class TrainingModelTest(TestCase):
    @classmethod
    def setUp(self):
        # Set up non-modified objects used by all test methods
        self.osm_user = baker.make(OsmUser, osm_id="123456789", username="testuser")
        self.dataset = baker.make(
            Dataset, name="Test Dataset", created_by=self.osm_user
        )
        self.model = baker.make(
            Model, name="Test Model", created_by=self.osm_user, dataset=self.dataset
        )
        self.training = baker.make(
            Training,
            model=self.model,
            zoom_level=[19, 20, 21, 22],
            created_by=self.osm_user,
            epochs=10,
            batch_size=32,
        )

    def test_training_creation(self):
        # Test the training instance has been created properly.
        self.assertTrue(isinstance(self.training, Training))
        self.assertIsNotNone(self.training)

    def test_string_representation(self):
        # Test the string representation of an AOI instance
        self.assertEqual(str(self.training), (self.model.name))

    def test_default_training_status(self):
        # Test the default status is "SUBMITTED"
        self.assertEqual(self.training.status, "SUBMITTED")


class FeedbackModelTest(TestCase):
    def setUp(self):
        # Set up non-modified objects used by all test methods
        self.osm_user = baker.make(OsmUser, osm_id="123456789", username="testuser")
        self.model = baker.make(
            Model,
            name="Test Model",
            created_by=self.osm_user,
            dataset=baker.make(Dataset, name="Test Dataset", created_by=self.osm_user),
        )
        self.feedback = baker.make(
            Feedback,
            user=self.osm_user,
            training=baker.make(
                Training,
                model=self.model,
                zoom_level=[19, 20, 21, 22],
                created_by=self.osm_user,
                epochs=10,
                batch_size=32,
            ),
            geom=Polygon(
                ((0, 0), (0, 1), (1, 1), (1, 0), (0, 0)),
                ((0.4, 0.4), (0.4, 0.6), (0.6, 0.6), (0.6, 0.4), (0.4, 0.4)),
            ),
            zoom_level=19,
            source_imagery="http://example.com/image.png",
        )

    def test_feedback_creation(self):
        # Test the feedback instance has been created properly.
        self.assertTrue(isinstance(self.feedback, Feedback))
        self.assertIsNotNone(self.feedback)

    def test_string_representation(self):
        # Test the string representation of a Feedback instance
        self.assertEqual(
            str(self.feedback),
            f"{self.feedback.user} - {self.feedback.training} - {self.feedback.feedback_type}",
        )

    def test_created_at_field(self):
        # Test the created_at field is not empty
        self.assertIsNotNone(self.feedback.created_at)


class FeedbackAOITest(TestCase):
    def setUp(self):
        # Set up non-modified objects used by all test methods
        self.osm_user = baker.make(OsmUser, osm_id="123456789", username="testuser")
        self.dataset = baker.make(
            Dataset, name="Test Dataset", created_by=self.osm_user
        )
        self.model = baker.make(
            Model, name="Test Model", created_by=self.osm_user, dataset=self.dataset
        )
        self.training = baker.make(
            Training,
            model=self.model,
            zoom_level=[19, 20, 21, 22],
            created_by=self.osm_user,
            epochs=10,
            batch_size=32,
        )
        self.feedbackAOI = baker.make(
            FeedbackAOI,
            user=self.osm_user,
            training=self.training,
            source_imagery="http://example.com/aoi_image.png",
            geom=Polygon(
                ((0, 0), (0, 1), (1, 1), (1, 0), (0, 0)),
                ((0.4, 0.4), (0.4, 0.6), (0.6, 0.6), (0.6, 0.4), (0.4, 0.4)),
            ),
        )

    def test_feedback_aoi_creation(self):
        # Test the feedback aoi instance has been created properly.
        self.assertTrue(isinstance(self.feedbackAOI, FeedbackAOI))
        self.assertIsNotNone(self.feedbackAOI)

    def test_string_representation(self):
        # Test the string representation of a FeedbackAOI instance
        self.assertEqual(
            str(self.feedbackAOI),
            f"{self.feedbackAOI.user} - {self.feedbackAOI.training} - {self.feedbackAOI.source_imagery}",
        )

    def test_string_representation_with_different_source_imagery(self):
        # Test the string representation of a FeedbackAOI instance with a different source imagery
        self.feedbackAOI.source_imagery = "http://example.com/different_image.png"
        self.assertEqual(
            str(self.feedbackAOI),
            f"{self.feedbackAOI.user} - {self.feedbackAOI.training} - {self.feedbackAOI.source_imagery}",
        )

    def test_string_representation_with_different_user(self):
        # Test the string representation of a FeedbackAOI instance with a different user
        self.feedbackAOI.user = baker.make(
            OsmUser, osm_id="987654321", username="differentuser"
        )
        self.assertEqual(
            str(self.feedbackAOI),
            f"{self.feedbackAOI.user} - {self.feedbackAOI.training} - {self.feedbackAOI.source_imagery}",
        )

    def test_string_representation_with_different_training(self):
        # Test the string representation of a FeedbackAOI instance with a different training
        self.feedbackAOI.training = baker.make(
            Training,
            model=self.feedbackAOI.training.model,
            zoom_level=[18, 19, 20, 21],
            created_by=self.feedbackAOI.training.created_by,
            epochs=5,
            batch_size=16,
        )
        self.assertEqual(
            str(self.feedbackAOI),
            f"{self.feedbackAOI.user} - {self.feedbackAOI.training} - {self.feedbackAOI.source_imagery}",
        )


class FeedbackLabelTest(TestCase):
    def setUp(self):
        # Set up non-modified objects used by all test methods
        self.osm_user = baker.make(
            OsmUser, osm_id="987654321", username="feedbacklabeluser"
        )
        self.dataset = baker.make(
            Dataset, name="Feedback Label Dataset", created_by=self.osm_user
        )
        self.model = baker.make(
            Model,
            name="Feedback Label Model",
            created_by=self.osm_user,
            dataset=self.dataset,
        )
        self.training = baker.make(
            Training,
            model=self.model,
            zoom_level=[19, 20, 21, 22],
            created_by=self.osm_user,
            epochs=5,
            batch_size=16,
        )
        self.feedbackAOI = baker.make(
            FeedbackAOI,
            user=self.osm_user,
            training=self.training,
            source_imagery="http://example.com/feedback_aoi_image.png",
            geom=Polygon(
                ((0, 0), (0, 2), (2, 2), (2, 0), (0, 0)),
                ((0.5, 0.5), (0.5, 1.5), (1.5, 1.5), (1.5, 0.5), (0.5, 0.5)),
            ),
        )
        self.feedbackLabel = baker.make(
            FeedbackLabel,
            osm_id=123456789,
            feedback_aoi=self.feedbackAOI,
            tags={"natural": "tree"},
            geom=Polygon(((0.5, 0.5), (0.5, 1.5), (1.5, 1.5), (1.5, 0.5), (0.5, 0.5))),
        )

    def test_feedback_label_creation(self):
        # Test the feedback label instance has been created properly.
        self.assertTrue(isinstance(self.feedbackLabel, FeedbackLabel))
        self.assertIsNotNone(self.feedbackLabel)

    def test_feedback_label_fields(self):
clear        # Test the fields of the feedback label instance
        self.assertEqual(self.feedbackLabel.osm_id, 123456789)
        self.assertEqual(self.feedbackLabel.feedback_aoi, self.feedbackAOI)
        self.assertEqual(self.feedbackLabel.tags, {"natural": "tree"})
        self.assertTrue(isinstance(self.feedbackLabel.geom, Polygon))

    def test_string_representation_with_different_osm_id(self):
        # Test the string representation of a FeedbackLabel instance with a different osm_id
        self.feedbackLabel.osm_id = 987654321
        self.assertEqual(
            str(self.feedbackLabel),
            f"{self.feedbackLabel.osm_id} - {self.feedbackLabel.feedback_aoi} - {self.feedbackLabel.tags}",
        )

    def test_string_representation_with_different_tags(self):
        # Test the string representation of a FeedbackLabel instance with different tags
        self.feedbackLabel.tags = {"natural": "water"}
        self.assertEqual(
            str(self.feedbackLabel),
            f"{self.feedbackLabel.osm_id} - {self.feedbackLabel.feedback_aoi} - {self.feedbackLabel.tags}",
        )

    def test_string_representation_with_different_geom(self):
        # Test the string representation of a FeedbackLabel instance with different geom
        self.feedbackLabel.geom = Polygon(
            ((0.5, 0.5), (0.5, 1.5), (1.5, 1.5), (1.5, 0.5), (0.5, 0.5))
        )
        self.assertEqual(
            str(self.feedbackLabel),
            f"{self.feedbackLabel.osm_id} - {self.feedbackLabel.feedback_aoi} - {self.feedbackLabel.tags}",
        )
