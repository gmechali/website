# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
from unittest.mock import patch

from server.tests.routes.api.mock_data import MULTIPLE_PROPERTY_VALUES_RESPONSE
from server.tests.routes.api.mock_data import \
    MULTIPLE_PROPERTY_VALUES_RESPONSE_WITH_LANGUAGES
from server.tests.routes.api.mock_data import OSERVATION_POINT_RESPONSE
from server.tests.routes.api.mock_data import OSERVATION_WITHIN_POINT_RESPONSE
from server.tests.routes.api.mock_data import SAMPLE_PLACE_PAGE_CHART_CONFIG
from web_app import app


# TODO(gmechali): Break up these tests into the overview_table_test, place_charts_test and related_places_test.
class TestPlaceAPI(unittest.TestCase):
  """Tests for the Place API."""

  @patch('server.routes.shared_api.place.parent_places')
  @patch('server.lib.fetch.raw_property_values')
  @patch('server.lib.fetch.multiple_property_values')
  @patch('server.services.datacommons.obs_point')
  @patch('server.services.datacommons.obs_point_within')
  def test_dev_place_charts(self, mock_obs_point_within, mock_obs_point,
                            mock_multiple_property_values,
                            mock_raw_property_values, mock_parent_places):
    """Test the place_charts endpoint."""

    with app.app_context():
      # Sample place_dcid
      place_dcid = "country/USA"

      # Override the CHART_CONFIG with sample values
      app.config['CHART_CONFIG'] = SAMPLE_PLACE_PAGE_CHART_CONFIG

      # Mock obs_point call with a properly structured response
      mock_obs_point.return_value = OSERVATION_POINT_RESPONSE

      # Mock obs_point_within for finding child places existence check for map-based stat vars
      mock_obs_point_within.return_value = OSERVATION_WITHIN_POINT_RESPONSE

      mock_multiple_property_values.return_value = MULTIPLE_PROPERTY_VALUES_RESPONSE

      # Mock fetch.raw_property_values to return empty lists (no nearby or similar places)
      mock_raw_property_values.return_value = {place_dcid: []}

      mock_parent_places.return_value = {
          'dcid': 'northamerica',
          'parents': [{
              'type': 'Continent',
              'dcid': 'northamerica'
          }]
      }

      # Send a GET request to the new endpoint
      response = app.test_client().get(f'/api/dev-place/charts/{place_dcid}')

      # Check if the response is successful
      print(response)
      self.assertEqual(response.status_code, 200)

      # Check that the response data contains expected fields
      response_json = response.get_json()
      self.assertIn('blocks', response_json)
      self.assertIn('place', response_json)
      self.assertIn('categories', response_json)
      self.assertIn('charts', response_json['blocks'][0])

      # Check that the 'charts' field contains the expected number of charts
      # Two charts have data (Crime and one Education stat var), and each has a
      # related chart, so we expect four charts
      self.assertEqual(
          sum(len(block.get('charts',)) for block in response_json['blocks']),
          4)

      # Optionally, check that the charts have the correct titles
      block_titles = [block['title'] for block in response_json['blocks']]
      self.assertIn('United States: Total crime', block_titles)
      self.assertIn('United States: Education attainment', block_titles)

      # Check that the 'place' field contains correct place information
      self.assertEqual(response_json['place']['dcid'], place_dcid)
      self.assertEqual(response_json['place']['name'], 'United States')
      self.assertEqual(response_json['place']['types'], ['Country'])

      # Check that 'categories' contains expected categories
      categories = [
          category['translatedName'] for category in response_json['categories']
      ]
      self.assertIn('Crime', categories)
      self.assertIn('Education', categories)

      # Ensure the denominator is present in chart results
      self.assertEqual(1, len(response_json["blocks"][0]["denominator"]))

      # TODO(gmechali): Imrpove test coverage of intricacies of the place charts selection.
      self.assertIsNone(response_json["blocks"][1]["denominator"])

  @patch('server.routes.shared_api.place.parent_places')
  @patch('server.routes.dev_place.utils.fetch.raw_property_values')
  @patch('server.routes.dev_place.utils.fetch.multiple_property_values')
  @patch('server.routes.dev_place.utils.fetch.descendent_places')
  def test_related_places(self, mock_descendent_places,
                          mock_multiple_property_values,
                          mock_raw_property_values, mock_parent_places):
    """Test the /api/dev-place/related-places endpoint. Mocks fetch.* and dc.* calls."""

    with app.app_context():
      # Sample place_dcid
      place_dcid = 'country/USA'

      # Define side effects for mock_multiple_property_values
      mock_multiple_property_values.return_value = MULTIPLE_PROPERTY_VALUES_RESPONSE_WITH_LANGUAGES

      # Mock descendent_places to return child places
      mock_descendent_places.return_value = {
          'country/USA': ['geoId/06', 'geoId/07']
      }

      # Define side effects for mock_raw_property_values
      def mock_raw_property_values_side_effect(nodes, prop, out):
        if prop == 'nearbyPlaces' and out:
          # Return nearby places
          return {
              nodes[0]: [{
                  'value': 'country/CAN@10km'
              }, {
                  'value': 'country/MEX@20km'
              }]
          }
        elif prop == 'member' and out:
          # For similar places (cohort)
          return {
              'PlacePagesComparisonCountriesCohort': [{
                  'dcid': 'country/GBR',
                  'types': ['Country']
              }, {
                  'dcid': 'country/AUS',
                  'types': ['Country']
              }]
          }
        else:
          return {node: [] for node in nodes}

      mock_raw_property_values.side_effect = mock_raw_property_values_side_effect

      # Define side effects for mock_parent_places_
      def mock_parent_places_side_effect(dcids, include_admin_areas):
        return {
            'dcid': 'geoId/06',
            'parents': [{
                'type': 'Country',
                'dcid': 'country/USA'
            }]
        }

      mock_parent_places.side_effect = mock_parent_places_side_effect

      # Send a GET request to the related-places endpoint
      response = app.test_client().get(
          f'/api/dev-place/related-places/{place_dcid}')

      # Check that the response is successful
      self.assertEqual(response.status_code, 200)

      # Parse the response JSON
      response_json = response.get_json()

      # Check that the response contains the expected fields
      self.assertIn('childPlaceType', response_json)
      self.assertIn('childPlaces', response_json)
      self.assertIn('nearbyPlaces', response_json)
      self.assertIn('place', response_json)
      self.assertIn('similarPlaces', response_json)
      self.assertIn('parentPlaces', response_json)

      # Check the place field
      self.assertEqual(response_json['place']['dcid'], place_dcid)
      self.assertEqual(response_json['place']['name'],
                       f'United States of America')
      self.assertEqual(response_json['place']['types'], ['Country'])

      # Check lengths of the place lists
      self.assertEqual(len(response_json['childPlaces']), 2)
      self.assertEqual(len(response_json['nearbyPlaces']), 2)
      self.assertEqual(len(response_json['similarPlaces']), 2)

      # Sort the childPlaces list by dcid
      response_json['childPlaces'].sort(key=lambda x: x['dcid'])

      # Check contents of childPlaces
      self.assertEqual(response_json['childPlaces'][0]['dcid'], 'geoId/06')
      self.assertEqual(response_json['childPlaces'][0]['name'], 'California')
      self.assertEqual(response_json['childPlaces'][0]['types'], ['State'])
      self.assertEqual(response_json['childPlaces'][1]['dcid'], 'geoId/07')
      self.assertEqual(response_json['childPlaces'][1]['name'], 'New York')
      self.assertEqual(response_json['childPlaces'][1]['types'], ['State'])

      # Check contents of nearbyPlaces
      self.assertEqual(response_json['nearbyPlaces'][0]['dcid'], 'country/CAN')
      self.assertEqual(response_json['nearbyPlaces'][0]['name'], 'Canada')
      self.assertEqual(response_json['nearbyPlaces'][0]['types'], ['Country'])

      # Check contents of similarPlaces
      self.assertEqual(response_json['similarPlaces'][0]['dcid'], 'country/GBR')
      self.assertEqual(response_json['similarPlaces'][0]['name'],
                       'United Kingdom')
      self.assertEqual(response_json['similarPlaces'][0]['types'], ['Country'])

      # Check the 'childPlaceType' field
      self.assertEqual(response_json['childPlaceType'], "State")

  @patch('server.routes.shared_api.place.parent_places')
  @patch('server.routes.dev_place.utils.fetch.raw_property_values')
  @patch('server.routes.dev_place.utils.fetch.multiple_property_values')
  @patch('server.routes.dev_place.utils.fetch.descendent_places')
  def test_related_places_es_locale(self, mock_descendent_places,
                                    mock_multiple_property_values,
                                    mock_raw_property_values,
                                    mock_parent_places):
    """Test the /api/dev-place/related-places endpoint with 'es' locale."""
    with app.app_context():
      # Sample place_dcid
      place_dcid = 'country/USA'

      # Define side effects for mock_multiple_property_values
      def mock_multiple_property_values_side_effect(nodes, props):
        result = {}
        for dcid in nodes:
          result[dcid] = {}
          if 'typeOf' in props:
            if dcid == place_dcid:
              result[dcid]['typeOf'] = ['Country']
            elif dcid in [
                'country/CAN', 'country/MEX', 'country/GBR', 'country/AUS'
            ]:
              result[dcid]['typeOf'] = ['Country']
            elif dcid in ['geoId/06', 'geoId/07']:
              result[dcid]['typeOf'] = ['State']
            else:
              result[dcid]['typeOf'] = ['Place']
          if 'name' in props:
            result[dcid]['name'] = [f'Name of {dcid}']
          if 'nameWithLanguage' in props:
            if dcid == place_dcid:
              result[dcid]['nameWithLanguage'] = [f'Nombre de {dcid}@es']
            elif dcid in ['geoId/06', 'country/CAN']:
              result[dcid]['nameWithLanguage'] = [f'Nombre de {dcid}@es']
            else:
              result[dcid]['nameWithLanguage'] = []
        return result

      mock_multiple_property_values.side_effect = mock_multiple_property_values_side_effect

      # Define side effects for mock_raw_property_values
      def mock_raw_property_values_side_effect(nodes, prop, out):
        if prop == 'containedInPlace' and not out:
          # Return child places
          return {
              nodes[0]: [{
                  'dcid': 'geoId/06',
                  'types': ['State']
              }, {
                  'dcid': 'geoId/07',
                  'types': ['State']
              }]
          }
        elif prop == 'nearbyPlaces' and out:
          # Return nearby places
          return {
              nodes[0]: [{
                  'value': 'country/CAN@10km'
              }, {
                  'value': 'country/MEX@20km'
              }]
          }
        elif prop == 'member' and out:
          # For similar places (cohort)
          if nodes == ['PlacePagesComparisonCountriesCohort']:
            return {
                'PlacePagesComparisonCountriesCohort': [{
                    'dcid': 'country/GBR',
                    'types': ['Country']
                }, {
                    'dcid': 'country/AUS',
                    'types': ['Country']
                }]
            }
          else:
            return {node: [] for node in nodes}
        else:
          return {node: [] for node in nodes}

      mock_raw_property_values.side_effect = mock_raw_property_values_side_effect

      # Define side effects for mock_parent_places_
      def mock_parent_places_side_effect(dcids, include_admin_areas):
        return {
            'dcid': 'geoId/06',
            'parents': [{
                'type': 'Country',
                'dcid': 'country/USA'
            }]
        }

      mock_parent_places.side_effect = mock_parent_places_side_effect

      mock_descendent_places.return_value = {
          'country/USA': ['geoId/06', 'geoId/07']
      }

      # Send a GET request to the api/dev-place/related-places endpoint with locale 'es'
      response = app.test_client().get(
          f'/api/dev-place/related-places/{place_dcid}?hl=es')

      # Check that the response is successful
      self.assertEqual(response.status_code, 200)

      # Parse the response JSON
      response_json = response.get_json()

      # Check that the response contains the expected fields
      self.assertIn('childPlaceType', response_json)
      self.assertIn('childPlaces', response_json)
      self.assertIn('nearbyPlaces', response_json)
      self.assertIn('place', response_json)
      self.assertIn('similarPlaces', response_json)

      # Check the place field
      self.assertEqual(response_json['place']['dcid'], place_dcid)
      # The name should be in Spanish if available
      self.assertEqual(response_json['place']['name'],
                       f'Nombre de {place_dcid}')
      self.assertEqual(response_json['place']['types'], ['Country'])

      # Check lengths of the place lists
      self.assertEqual(len(response_json['childPlaces']), 2)
      self.assertEqual(len(response_json['nearbyPlaces']), 2)
      self.assertEqual(len(response_json['similarPlaces']), 2)

      # Sort the list to ensure the right values.
      response_json['childPlaces'].sort(key=lambda x: x['dcid'])

      # Check contents of childPlaces
      # First child place should have Spanish name
      self.assertEqual(response_json['childPlaces'][0]['dcid'], 'geoId/06')
      self.assertEqual(response_json['childPlaces'][0]['name'],
                       'Nombre de geoId/06')
      self.assertEqual(response_json['childPlaces'][0]['types'], ['State'])
      # Second child place defaults to English name
      self.assertEqual(response_json['childPlaces'][1]['dcid'], 'geoId/07')
      self.assertEqual(response_json['childPlaces'][1]['name'],
                       'Name of geoId/07')
      self.assertEqual(response_json['childPlaces'][1]['types'], ['State'])

      # Check contents of nearbyPlaces
      # First child place should have Spanish name
      self.assertEqual(response_json['nearbyPlaces'][0]['dcid'], 'country/CAN')
      self.assertEqual(response_json['nearbyPlaces'][0]['name'],
                       'Nombre de country/CAN')
      self.assertEqual(response_json['nearbyPlaces'][0]['types'], ['Country'])

      # Check contents of similarPlaces
      # Similar places default to English names
      self.assertEqual(response_json['similarPlaces'][0]['dcid'], 'country/GBR')
      self.assertEqual(response_json['similarPlaces'][0]['name'],
                       'Name of country/GBR')
      self.assertEqual(response_json['similarPlaces'][0]['types'], ['Country'])

      # Check the 'childPlaceType' field
      self.assertEqual(response_json['childPlaceType'], "State")
