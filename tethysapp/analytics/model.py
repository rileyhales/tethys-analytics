def user_points_json():
    """
    gets a list of latitude and longitude points from Google Analytics and writes a json object to users_layer.js where
    it can be used by the map on the main page of the app for showing user locations.

    1. query google analytics to get the list of latitudes and longitudes
    2. makes a list of tuples of the form (LONGitude, LATitude). must be longitude (x) then latitude (y)
    3. uses json to dump the object to the js file
    """
    import geojson, json, ast, os
    from googleAnalytics import GAstats

    mapinfo = ['ga:latitude', 'ga:longitude']
    mapinfo = GAstats(mapinfo)

    lat = ast.literal_eval(str(mapinfo['ga:latitude']))
    lon = ast.literal_eval(str(mapinfo['ga:longitude']))

    latlons = []
    latlons.append((lon, lat))

    points = geojson.MultiPoint(latlons)
    filepath = os.path.join(os.path.dirname(__file__), 'public/js/users_layer.js')
    with open(filepath, 'w') as js:
        js.write('users_layer=' + json.dumps(points))

    return
