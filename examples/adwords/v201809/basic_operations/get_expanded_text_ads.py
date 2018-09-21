#!/usr/bin/env python
#
# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This example gets all expanded text ads for a given ad group.

To add an expanded text ad, run add_expanded_text_ads.py.

The LoadFromStorage method is pulling credentials and properties from a
"googleads.yaml" file. By default, it looks for this file in your home
directory. For more information, see the "Caching authentication information"
section of our README.

"""

from googleads import adwords


PAGE_SIZE = 500
AD_GROUP_ID = 'INSERT_AD_GROUP_ID_HERE'


def main(client, ad_group_id):
  # Initialize appropriate service.
  ad_group_ad_service = client.GetService('AdGroupAdService', version='v201809')

  # Construct selector and get all ads for a given ad group.
  offset = 0
  selector = {
      'fields': ['Id', 'AdGroupId', 'Status', 'HeadlinePart1', 'HeadlinePart2',
                 'Description'],
      'predicates': [
          {
              'field': 'AdGroupId',
              'operator': 'EQUALS',
              'values': [ad_group_id]
          },
          {
              'field': 'AdType',
              'operator': 'EQUALS',
              'values': ['EXPANDED_TEXT_AD']
          }
      ],
      'paging': {
          'startIndex': str(offset),
          'numberResults': str(PAGE_SIZE)
      },
      'ordering': [
          {
              'field': 'Id',
              'sortOrder': 'ASCENDING'
          }
      ]
  }
  more_pages = True
  while more_pages:
    page = ad_group_ad_service.get(selector)

    # Display results.
    if 'entries' in page:
      for ad in page['entries']:
        print ('ExpandedTextAd with id "%d", AdGroupId "%d", status "%s", '
               'headlinePart1 "%s", headlinePart2 "%s", description "%s" was '
               'found.' % (ad['ad']['id'], ad['adGroupId'], ad['status'],
                           ad['ad']['headlinePart1'], ad['ad']['headlinePart2'],
                           ad['ad']['description']))
    else:
      print 'No ads were found.'
    offset += PAGE_SIZE
    selector['paging']['startIndex'] = str(offset)
    more_pages = offset < int(page['totalNumEntries'])


if __name__ == '__main__':
  # Initialize client object.
  adwords_client = adwords.AdWordsClient.LoadFromStorage()

  main(adwords_client, AD_GROUP_ID)
