SAMPLE_DATE = '2025-05-01'

SAMPLE_PARAMS = {
    'geo': 'US',
    'q': 'vpn,antivirus,ad blocker,password manager',
}

SAMPLE_RESPONSE = {
    "search_metadata": {
        "id": "6820fea3acb3e484a45c78cb",
        "status": "Success",
        "json_endpoint": "https://serpapi.com/searches/311e15b5bdcf2053/6820fea3acb3e484a45c78cb.json",
        "created_at": "2025-05-11 19:46:43 UTC",
        "processed_at": "2025-05-11 19:46:43 UTC",
        "google_trends_url": "https://trends.google.com/trends/embed/explore/TIMESERIES?hl=en&tz=420&req=%7B%22comparisonItem%22%3A%5B%7B%22keyword%22%3A%22vpn%22%2C%22geo%22%3A%22US%22%2C%22time%22%3A%222025-05-01+2025-05-01%22%7D%2C%7B%22keyword%22%3A%22antivirus%22%2C%22geo%22%3A%22US%22%2C%22time%22%3A%222025-05-01+2025-05-01%22%7D%2C%7B%22keyword%22%3A%22ad+blocker%22%2C%22geo%22%3A%22US%22%2C%22time%22%3A%222025-05-01+2025-05-01%22%7D%2C%7B%22keyword%22%3A%22password+manager%22%2C%22geo%22%3A%22US%22%2C%22time%22%3A%222025-05-01+2025-05-01%22%7D%5D%2C%22category%22%3A0%2C%22property%22%3A%22%22%7D",
        "raw_html_file": "https://serpapi.com/searches/311e15b5bdcf2053/6820fea3acb3e484a45c78cb.html",
        "prettify_html_file": "https://serpapi.com/searches/311e15b5bdcf2053/6820fea3acb3e484a45c78cb.prettify",
        "total_time_taken": 2.14
    },
    "search_parameters": {
        "engine": "google_trends",
        "q": "vpn,antivirus,ad blocker,password manager",
        "hl": "en",
        "geo": "US",
        "date": "2025-05-01 2025-05-01",
        "tz": "420",
        "data_type": "TIMESERIES"
    },
    "interest_over_time": {
        "timeline_data": [
            {
            "date": "May 1, 2025",
            "timestamp": "1746057600",
            "values": [
                {
                    "query": "vpn",
                    "value": "100",
                    "extracted_value": 100
                },
                {
                    "query": "antivirus",
                    "value": "14",
                    "extracted_value": 14
                },
                {
                    "query": "ad blocker",
                    "value": "9",
                    "extracted_value": 9
                },
                {
                    "query": "password manager",
                    "value": "31",
                    "extracted_value": 31
                }
            ]
          }
        ],
    "averages": [
        {
            "query": "vpn",
            "value": 100
        },
        {
            "query": "antivirus",
            "value": 14
        },
        {
            "query": "ad blocker",
            "value": 9
        },
        {
            "query": "password manager",
            "value": 31
        }
    ]}
}

SAMPLE_TRANSFORMED_RESPONSE = [
    {
        "query": "vpn",
        "extracted_value": 100
    },
    {
        "query": "antivirus",
        "extracted_value": 14
    },
    {
        "query": "ad blocker",
        "extracted_value": 9
    },
    {
        "query": "password manager",
        "extracted_value": 31
    }
]

SAMPLE_BAD_RESPONSE = {
    "search_metadata": {
        "id": "6820fea3acb3e484a45c78cb",
        "status": "Success",
        "json_endpoint": "https://serpapi.com/searches/311e15b5bdcf2053/6820fea3acb3e484a45c78cb.json",
        "created_at": "2025-05-11 19:46:43 UTC",
        "processed_at": "2025-05-11 19:46:43 UTC",
        "google_trends_url": "https://trends.google.com/trends/embed/explore/TIMESERIES?hl=en&tz=420&req=%7B%22comparisonItem%22%3A%5B%7B%22keyword%22%3A%22vpn%22%2C%22geo%22%3A%22US%22%2C%22time%22%3A%222025-05-01+2025-05-01%22%7D%2C%7B%22keyword%22%3A%22antivirus%22%2C%22geo%22%3A%22US%22%2C%22time%22%3A%222025-05-01+2025-05-01%22%7D%2C%7B%22keyword%22%3A%22ad+blocker%22%2C%22geo%22%3A%22US%22%2C%22time%22%3A%222025-05-01+2025-05-01%22%7D%2C%7B%22keyword%22%3A%22password+manager%22%2C%22geo%22%3A%22US%22%2C%22time%22%3A%222025-05-01+2025-05-01%22%7D%5D%2C%22category%22%3A0%2C%22property%22%3A%22%22%7D",
        "raw_html_file": "https://serpapi.com/searches/311e15b5bdcf2053/6820fea3acb3e484a45c78cb.html",
        "prettify_html_file": "https://serpapi.com/searches/311e15b5bdcf2053/6820fea3acb3e484a45c78cb.prettify",
        "total_time_taken": 2.14
    },
    "search_parameters": {
        "engine": "google_trends",
        "q": "vpn,antivirus,ad blocker,password manager",
        "hl": "en",
        "geo": "US",
        "date": "2025-05-01 2025-05-01",
        "tz": "420",
        "data_type": "TIMESERIES"
    },
    "interest_over_time": {
        "timeline_data": [
            {
            "date": "May 1, 2025",
            "timestamp": "1746057600",
            "values": [
                {
                    "query": "vpn",
                    "value": "100",
                    "extracted_value": None
                },
                {
                    "query": "antivirus",
                    "value": "14",
                    "extracted_value": None
                },
                {
                    "query": "ad blocker",
                    "value": "9",
                    "extracted_value": None
                },
                {
                    "query": "password manager",
                    "value": "31",
                    "extracted_value": None
                }
            ]
          }
        ],
    "averages": [
        {
            "query": "vpn",
            "value": 100
        },
        {
            "query": "antivirus",
            "value": 14
        },
        {
            "query": "ad blocker",
            "value": 9
        },
        {
            "query": "password manager",
            "value": 31
        }
    ]}
}

SAMPLE_PARAMS_DIFFERENT = {
    'geo': 'GB',
    'q': 'vpn,antivirus,ad blocker,password manager,antimalware',
}

SAMPLE_RESPONSE_DIFFERENT = {
    "search_metadata": {
        "id": "6820fea3acb3e484a45c78cb",
        "status": "Success",
        "json_endpoint": "https://serpapi.com/searches/311e15b5bdcf2053/6820fea3acb3e484a45c78cb.json",
        "created_at": "2025-05-11 19:46:43 UTC",
        "processed_at": "2025-05-11 19:46:43 UTC",
        "google_trends_url": "https://trends.google.com/trends/embed/explore/TIMESERIES?hl=en&tz=420&req=%7B%22comparisonItem%22%3A%5B%7B%22keyword%22%3A%22vpn%22%2C%22geo%22%3A%22US%22%2C%22time%22%3A%222025-05-01+2025-05-01%22%7D%2C%7B%22keyword%22%3A%22antivirus%22%2C%22geo%22%3A%22US%22%2C%22time%22%3A%222025-05-01+2025-05-01%22%7D%2C%7B%22keyword%22%3A%22ad+blocker%22%2C%22geo%22%3A%22US%22%2C%22time%22%3A%222025-05-01+2025-05-01%22%7D%2C%7B%22keyword%22%3A%22password+manager%22%2C%22geo%22%3A%22US%22%2C%22time%22%3A%222025-05-01+2025-05-01%22%7D%5D%2C%22category%22%3A0%2C%22property%22%3A%22%22%7D",
        "raw_html_file": "https://serpapi.com/searches/311e15b5bdcf2053/6820fea3acb3e484a45c78cb.html",
        "prettify_html_file": "https://serpapi.com/searches/311e15b5bdcf2053/6820fea3acb3e484a45c78cb.prettify",
        "total_time_taken": 2.14
    },
    "search_parameters": {
        "engine": "google_trends",
        "q": "vpn,antivirus,ad blocker,password manager,antimalware",
        "hl": "en",
        "geo": "GB",
        "date": "2025-05-01 2025-05-01",
        "tz": "420",
        "data_type": "TIMESERIES"
    },
    "interest_over_time": {
        "timeline_data": [
            {
            "date": "May 1, 2025",
            "timestamp": "1746057600",
            "values": [
                {
                    "query": "vpn",
                    "value": "100",
                    "extracted_value": 100
                },
                {
                    "query": "antivirus",
                    "value": "14",
                    "extracted_value": 14
                },
                {
                    "query": "ad blocker",
                    "value": "9",
                    "extracted_value": 9
                },
                {
                    "query": "password manager",
                    "value": "31",
                    "extracted_value": 31
                },
                {
                    "query": "antimalware",
                    "value": "1",
                    "extracted_value": 1
                }
            ]
          }
        ],
    "averages": [
        {
            "query": "vpn",
            "value": 100
        },
        {
            "query": "antivirus",
            "value": 14
        },
        {
            "query": "ad blocker",
            "value": 9
        },
        {
            "query": "password manager",
            "value": 31
        },
        {
            "query": "antimalware",
            "value": 1
        }
    ]}
}
