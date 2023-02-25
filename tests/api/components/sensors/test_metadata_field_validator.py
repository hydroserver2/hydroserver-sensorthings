from django.test import TestCase
from sensorthings.core.components import metadata_validator


class MetadataFieldValidatorTest(TestCase):

    def test_valid_metadata(self):
        """
        Runs the metadata validator on a valid metadata value and corresponding encoding type. The validator should
        return the original value without raising a ValidationError.
        """

        raw_value = 'http://www.example.com/test.pdf'

        validated_value = metadata_validator(
            value=raw_value,
            values={
                'encoding_type': 'application/pdf'
            }
        )

        self.assertEqual(raw_value, validated_value)

    def test_invalid_metadata(self):
        """
        Runs the metadata validator on an invalid metadata value. The validator should raise a ValueError.
        """

        raw_value = 'not/a/valid/url.pdf'

        self.assertRaises(
            ValueError,
            metadata_validator,
            value=raw_value,
            values={
                'encoding_type': 'application/pdf'
            }
        )

    def test_metadata_type_mismatch(self):
        """
        Runs the metadata validator on a valid metadata value with the wrong encoding type. The validator should raise
        a ValueError.
        """

        raw_value = 'https://www.example.com/test.xml'

        self.assertRaises(
            ValueError,
            metadata_validator,
            value=raw_value,
            values={
                'encoding_type': 'application/pdf'
            }
        )
