import unittest
from unittest.mock import patch
import requests

# Import the functions you want to test
from brevium import (
    get_curr_schedule,
    valid_appointment_time,
    valid_appointment,
    is_week_apart,
    doctor_is_available
)

class TestAppointmentScheduling(unittest.TestCase):
    def test_get_curr_schedule(self):
        # Mock a response for the external API
        class MockResponse:
            def __init__(self, status_code, json_data):
                self.status_code = status_code
                self.json_data = json_data

            def json(self):
                return self.json_data

        # Mock a successful API response
        mock_data = [
            {
                'doctorId': 1,
                'personId': 101,
                'appointmentTime': '2021-11-05T10:00:00+0000'
            },
            {
                'doctorId': 1,
                'personId': 102,
                'appointmentTime': '2021-11-06T14:00:00+0000'
            }
        ]

        mock_response = MockResponse(200, mock_data)

        # Mock the requests.get function to return the mock response
        with patch('requests.get', return_value=mock_response):
            appointments = get_curr_schedule()

        # Define expected result
        expected_result = {
            1: {101: ['2021-11-05T10:00:00+0000'], 102: ['2021-11-06T14:00:00+0000']}
        }

        self.assertEqual(appointments, expected_result)

    def test_valid_appointment_time(self):
        # Test a valid appointment time for a new patient
        self.assertTrue(valid_appointment_time('2021-11-05T15:00:00+0000', isNew=True))

        # Test an invalid appointment time for a new patient
        self.assertFalse(valid_appointment_time('2021-11-05T10:30:00+0000', isNew=True))

    def test_valid_appointment(self):
        # Mock an appointments dictionary for testing
        appointments = {
            1: {101: ['2021-11-05T10:00:00+0000'], 102: ['2021-11-06T14:00:00+0000']}
        }

        # Test a valid appointment for an existing patient with a week gap
        self.assertTrue(valid_appointment(appointments, '2021-11-13T10:00:00+0000', 101))

        # Test an invalid appointment for an existing patient with less than a week gap
        self.assertFalse(valid_appointment(appointments, '2021-11-08T15:00:00+0000', 101))

    def test_is_week_apart(self):
        # Test two appointments that are exactly one week apart
        self.assertTrue(is_week_apart('2021-11-05T10:00:00+0000', '2021-11-12T10:00:00+0000'))

        # Test two appointments that are less than one week apart
        self.assertFalse(is_week_apart('2021-11-05T10:00:00+0000', '2021-11-11T10:00:00+0000'))

        # Test two appointments that are more than one week apart
        self.assertTrue(is_week_apart('2021-11-05T10:00:00+0000', '2021-11-20T10:00:00+0000'))

    def test_doctor_is_available(self):
        # Mock an appointments dictionary for testing
        appointments = {
            1: {101: ['2021-11-05T10:00:00+0000', '2021-11-12T14:00:00+0000']},
            2: {103: ['2021-11-05T15:00:00+0000']}
        }

        # Test a doctor's availability at a specific time
        self.assertTrue(doctor_is_available(1, '2021-11-13T10:00:00+0000', appointments))

        # Test a doctor's unavailability at a specific time
        self.assertFalse(doctor_is_available(2, '2021-11-05T15:00:00+0000', appointments))

if __name__ == '__main__':
    unittest.main()
