from django.shortcuts import render
from django.conf import settings
import requests

def location_dash(request):
    try:
        response = requests.get("http://job-db.docker.local/state/jobs")
        state =  response.json()
        response = requests.get("http://job-db.docker.local/state/locations")
        locations_raw = response.json()
        locations = []

        fields_shown = settings.LOC_FIELDS_SHOWN
        field_names = settings.LOC_FIELD_NAMES
        fields = {'shown':fields_shown,'names':field_names}

        for entry in locations_raw:
            locations += [ entry['name'] ]

        return render(
                request,
                'locations.html',
                {
                    'fields':fields,
                    'locations':locations,
                    'jobstate':state,
                    'sort':'descending' if settings.SORT_ORDER_DESCENDING else 'ascending',
                    'show_duration':'true' if settings.SHOW_DURATION else 'false',
                    'id_as_link':'true' if settings.ID_AS_LINK else 'false',
                    'id_link_template':settings.LINK_TEMPLATE,
                }
            )
    except ConnectionRefusedError:
        return render(request,"error.html",{"reason":"Can't reach database right now - try refreshing in a few seconds"})

def job_dash(request):
    response = requests.get("http://job-db.docker.local/state/jobs")
    state = response.json()

    fields_shown = settings.JOB_FIELDS_SHOWN
    field_names = settings.JOB_FIELD_NAMES

    fields = {'shown':fields_shown,'names':field_names}

    return render(
            request,
            'jobs.html',
            {
                'fields':fields,
                'jobstate':state,
                'sort':'descending' if settings.SORT_ORDER_DESCENDING else 'ascending',
                'show_duration':'true' if settings.SHOW_DURATION else 'false',
                'id_as_link':'true' if settings.ID_AS_LINK else 'false',
                'id_link_template':settings.LINK_TEMPLATE,
            }
        )
