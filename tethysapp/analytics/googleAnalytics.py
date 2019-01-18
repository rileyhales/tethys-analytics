import os
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

"""Hello Analytics Reporting API V4."""

"""
To make an API call, you need to
1. Call GAstats and provide a list of the metrics and dimensions you want to query. GAstats does the following:
    1. uses sortMetricDimension to appropriately filter them to make a correctly formated request
    2. call init analytics to get an analytics response object
    3. call get_report to actually get the information from GA
    4. returns the raw/unfiltered report of information from google
2. Filter the response information to get the parts you're interested in.
3. Use/display the data in your code
"""

######## THE NEXT 4 FUNCTIONS ARE USED TO MAKE A GENERAL QUERY OF THE GOOGLE ANALYTICS API ########

def init_analytics(key_location, scopes):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        key_location, scopes)

    # Build the service object.
    analytics = build('analyticsreporting', 'v4', credentials=credentials)

    return analytics


def get_report(analytics, viewID, metrics, dimensions):
    reports = analytics.reports().batchGet(
        body={
            'reportRequests': [{
                'viewId': viewID,
                'dateRanges': [{'startDate': '30daysAgo', 'endDate': 'today'}],
                'metrics': metrics,
                'dimensions': dimensions
                }]
            }
        ).execute()
    return reports


def sortMetricDimension(selections):
    from .tools import supportedMetricsDimensions
    supported = supportedMetricsDimensions()
    metric_list = supported['metrics']
    dimension_list = supported['dimensions']
    metrics = []
    dimensions = []
    for selection in selections:
        if selection in metric_list:
            tmp = {'expression': selection}
            metrics.append(tmp)
        if selection in dimension_list:
            tmp = {'name': selection}
            dimensions.append(tmp)

    sorted = {
        'metrics': metrics,
        'dimensions': dimensions,
    }

    return sorted

def GAstats(selections):
    """
    selections: a list in the form ['name of metric 1', 'name of metric 2', ... ] containing all the metrics and
                dimensions to be queried. Metrics and Dimensions will be appropriately sorted.
    """
    # Sort the user provided information
    selections = sortMetricDimension(selections)
    metrics = selections['metrics']
    dimensions = selections['dimensions']
    # set the environment for getting data from google analytics
    scopes = ['https://www.googleapis.com/auth/analytics.readonly']
    key_location = os.path.join(os.path.dirname(__file__), 'workspaces/app_workspace/api_info.json')
    viewID = '184214759'    # my accounts
    # viewID = '185555963'    # the worldwater account
    # make the queries and print the results
    analytics = init_analytics(key_location, scopes)
    response = get_report(analytics, viewID, metrics, dimensions)

    return response


###### THE FOLLOWING FUNCTIONS WILL CALL GASTATS WITH PREDEFINED WAYS TO FILTER THE RESPONSE DATA #######


def print_results(response):
    """Parses and prints the Analytics Reporting API V4 response.
    Args:
      response: An Analytics Reporting API V4 response.
    """
    results = {}

    for report in response.get('reports', []):
        columnHeader = report.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [])
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

        for row in report.get('data', {}).get('rows', []):
            dimensions = row.get('dimensions', [])
            dateRangeValues = row.get('metrics', [])

            for header, dimension in zip(dimensionHeaders, dimensions):
                results[header] = dimension

            for i, values in enumerate(dateRangeValues):
                for metricHeader, value in zip(metricHeaders, values.get('values')):
                    results[metricHeader.get('name')] = value

    return results
