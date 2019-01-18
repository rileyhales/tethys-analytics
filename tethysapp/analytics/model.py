def lonlat_list():
    """
    gets a list of latitude and longitude points from Google Analytics and writes a json object to users_layer.js where
    it can be used by the map on the main page of the app for showing user locations.

    1. query google analytics to get the list of latitudes and longitudes
    2. makes a list of tuples of the form (LONGitude, LATitude). must be longitude (x) then latitude (y)
    3. uses json to dump the object to the js file
    """

    import geojson, json, os
    from .googleAnalytics import GAstats

    print('Generating a GeoJSON user locations file')

    response = GAstats(['ga:longitude', 'ga:latitude'])
    results = response.get('reports', [])[0]['data']['rows']

    lonlats = []
    for i in range(len(results)):
        pair = results[i]['dimensions']
        entry = (float(pair[0]), float(pair[1]))
        lonlats.append(entry)

    points = geojson.MultiPoint(lonlats)
    filepath = os.path.join(os.path.dirname(__file__), 'public/js/users_layer.js')
    with open(filepath, 'w') as js:
        js.write('users_layer=' + json.dumps(points))

    return
