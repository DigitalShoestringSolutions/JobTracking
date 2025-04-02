# My Settings - default
LOC_FIELDS_SHOWN = ['id','time','user1']
LOC_FIELD_NAMES = {
            'id':'Job Number',
            'time':'Time',
            'user1':'Comment',
        }

JOB_FIELDS_SHOWN = ['id','location','time','user1']
JOB_FIELD_NAMES = {
            'id':'Job Number',
            'location':'Location',
            'time':'Time',
            'user1':'Comment',
        }


SORT_ORDER_DESCENDING = {{job_order}}
SHOW_DURATION = {{show_duration}}

ID_AS_LINK = False
LINK_TEMPLATE = 'function get_link_href(id,location){ return "" }'
