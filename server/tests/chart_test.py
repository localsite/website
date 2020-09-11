# Copyright 2020 Google LLC
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

import unittest
import json
from unittest.mock import patch

from main import app

class TestRoute(unittest.TestCase):

    @patch('routes.api.chart.dc_service.fetch_data')
    @patch('routes.api.chart.place_api.statsvars')
    def test_cache_necessary_dates(self, mock_stat_vars, mock_landing_page):
        mock_stat_vars.return_value = [
            'StatVar1',
            'StatVar2',
            'StatVar3',
            'StatVar4',
            'StatVar5',
            'StatVar6',
            'StatVar7',
            'StatVar8'
        ]
        mock_landing_page.return_value = {
            'geoId/06': {
                'StatVar1': {
                    'data': {
                        '2010': 200,
                        '2019': 200,
                        '2020': 200
                    }
                },
                'StatVar2': {
                    'data': {
                        '2017': 200,
                        '2018': 200,
                        '2019': 200
                    }
                },
                'StatVar3': {
                    'data': {
                        '2017': 200,
                        '2018': 200,
                        '2019': 200
                    }
                },
                'StatVar4': {
                    'data': {
                        '2016': 200,
                        '2018': 200,
                        '2020': 200
                    }
                },
                'StatVar5': {
                    'data': {
                        '2011': 200,
                        '2012': 200,
                        '2013': 200
                    }
                },
                'StatVar6': {
                    'data': {
                        '2018': 200,
                        '2019': 200,
                        '2020': 200
                    }
                },
                'StatVar7': {
                    'data': {
                        '2015': 200,
                        '2017': 200,
                        '2019': 200
                    }
                },
                'StatVar8': {
                    'data': {
                        '2018': 200,
                        '2019': 200,
                        '2020': 200
                    }
                },
            }
        }
        with app.app_context():
            app.config['CHART_CONFIG'] = [
                {
                    'label': 'Test',
                    'charts': [
                        {
                            'title': 'Test1',
                            "chartType": "GROUP_BAR",
                            "axis": "PLACE",
                            "statsVars": [
                              "StatVar1",
                              "StatVar2",
                              "StatVar3",
                              "StatVar4",
                              "StatVar5",
                            ]
                        }
                    ],
                    'children': [
                        {
                            'label': 'Test',
                            'charts': [
                                {
                                    'title': 'Test2',
                                    "chartType": "SINGLE_BAR",
                                    "statsVars": [
                                      "StatVar1",
                                      "StatVar2",
                                      "StatVar6",
                                      "StatVar7",
                                      "StatVar8",
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
            response = app.test_client().get('api/chart/config/geoId/06')
            assert response.status_code == 200
            assert json.loads(response.data)['data'] == {
                'geoId/06': {
                    'StatVar1': {
                        'data': {
                            '2019': 200,
                            '2020': 200
                        }
                    },
                    'StatVar2': {
                        'data': {
                            '2019': 200
                        }
                    },
                    'StatVar3': {
                        'data': {
                            '2019': 200
                        }
                    },
                    'StatVar4': {
                        'data': {
                            '2020': 200
                        }
                    },
                    'StatVar5': {
                        'data': {
                            '2013': 200
                        }
                    },
                    'StatVar6': {
                        'data': {
                            '2019': 200
                        }
                    },
                    'StatVar7': {
                        'data': {
                            '2019': 200
                        }
                    },
                    'StatVar8': {
                        'data': {
                            '2019': 200
                        }
                    }
                }
            }