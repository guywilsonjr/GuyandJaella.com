import boto3
import os
import time
import urllib.request

HTTPS = 'https://'


CW_TIME_MICROSECONDS_UNIT = 'Microseconds'
CW_TIME_MILLISECONDS_UNIT = 'Milliseconds'
TIME_NANOSECONDS_UNIT = 'Nanoseconds'
UNIT_TO_TIME_MULTIPLIER_MAP = { CW_TIME_MICROSECONDS_UNIT: 1, CW_TIME_MILLISECONDS_UNIT: 1000, TIME_NANOSECONDS_UNIT: 0.001}
MAIN_SITE_METRIC = ('MainSite', 'Latency', CW_TIME_MICROSECONDS_UNIT, '#FF0000')
SIDEBAR_SITE_METRIC = ('Sidebar', 'Latency', CW_TIME_MICROSECONDS_UNIT, '#1E90FF')
METRIC_NAME_FORMAT = '{} {}'
METRICS = {MAIN_SITE_METRIC, SIDEBAR_SITE_METRIC}

STATIC_URL_PREFIX = '{}{}/'.format(HTTPS, os.environ['STATIC_DOMAIN'])
STATIC_SITE_URL_PREFIX = '{}www.{}/'.format(HTTPS, os.environ['SITE_DOMAIN'])

MAIN_SITE_FILENAME = 'home.html'
SIDEBAR_ITEM_FILENAME = 'sidebar_item.html'

MAIN_SITE_FILE_TXT = '&lt;!DOCTYPE html> &lt;html lang="en"> &lt;head> &lt;meta charset="utf-8" /> &lt;meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no"> &lt;link rel="apple-touch-icon" sizes="76x76" href="assets/img/apple-icon.png"> &lt;link rel="icon" type="image/png" href="assets/img/favicon.png"> &lt;title> Guy and Jaella &lt;/title> &lt;!-- Fonts and icons --> &lt;link href="https://fonts.googleapis.com/css?family=Poppins:200,300,400,600,700,800" rel="stylesheet" /> &lt;link href="https://use.fontawesome.com/releases/v5.0.6/css/all.css" rel="stylesheet"> &lt;!-- Nucleo Icons --> &lt;link href="assets/css/nucleo-icons.css" rel="stylesheet" /> &lt;!-- CSS Files --> &lt;link href="assets/css/black-dashboard.css?v=1.0.0" rel="stylesheet" /> &lt;/head> &lt;body class="sidebar-mini"> &lt;div class="wrapper"> &lt;div class="sidebar"> &lt;div class="sidebar-wrapper"> &lt;div class="logo"> &lt;a href="javascript:void(0)" class="simple-text logo-normal"> Menu &lt;/a> &lt;/div> &lt;ul class="nav"> {SIDEBAR_ITEMS} &lt;/ul> &lt;/div> &lt;/div> &lt;div class="main-panel"> &lt;!-- End Navbar --> &lt;div class="col-md-5" style="margin: auto;top: 20%"> &lt;/style>> &lt;div class="card card-user"> &lt;div class="card-body"> &lt;p class="card-text"> &lt;div class="author"> &lt;div class="block block-one">&lt;/div> &lt;div class="block block-two">&lt;/div> &lt;div class="block block-three">&lt;/div> &lt;div class="block block-four">&lt;/div> &lt;a href="javascript:void(0)"> &lt;img class="avatar" src="{GUY_AND_JAELLA_HOME_PIC}" alt="..." style="height: 500px; width:450px"> &lt;h5 class="title">The cutest couple ever&lt;/h5> &lt;/a> &lt;p class="description"> Guy And Jaella &lt;/p> &lt;/div> &lt;/p> &lt;div class="card-description" style="margin: auto; width: fit-content"> We found perfect love. We\'re meant for each other &lt;/div> &lt;/div> &lt;div class="card-footer"> &lt;div class="button-container"> &lt;button href="javascript:void(0)" class="btn btn-icon btn-round btn-facebook"> &lt;i class="fab fa-facebook">&lt;/i> &lt;/button> &lt;button href="javascript:void(0)" class="btn btn-icon btn-round btn-twitter"> &lt;i class="fab fa-twitter">&lt;/i> &lt;/button> &lt;button href="javascript:void(0)" class="btn btn-icon btn-round btn-google"> &lt;i class="fab fa-google-plus">&lt;/i> &lt;/button> &lt;/div> &lt;/div> &lt;/div> &lt;/div> &lt;/div> &lt;/div> &lt;/div> &lt;/div> &lt;/div> &lt;!-- Core JS Files --> &lt;script src="assets/js/core/jquery.min.js">&lt;/script> &lt;script src="assets/js/core/popper.min.js">&lt;/script> &lt;script src="assets/js/core/bootstrap.min.js">&lt;/script> &lt;script src="assets/js/plugins/perfect-scrollbar.jquery.min.js">&lt;/script> &lt;script src="assets/js/plugins/moment.min.js">&lt;/script> &lt;!-- Control Center for Black Dashboard: parallax effects, scripts for the example pages etc --> &lt;script src="assets/js/black-dashboard.min.js?v=1.0.0">&lt;/script> &lt;script> $(document).ready(function() { $().ready(function() { $sidebar = $(\'.sidebar\'); $navbar = $(\'.navbar\'); $main_panel = $(\'.main-panel\'); $full_page = $(\'.full-page\'); $sidebar_responsive = $(\'body > .navbar-collapse\'); sidebar_mini_active = true; white_color = false; window_width = $(window).width(); fixed_plugin_open = $(\'.sidebar .sidebar-wrapper .nav li.active a p\').html(); $(\'.fixed-plugin a\').click(function(event) { if ($(this).hasClass(\'switch-trigger\')) { if (event.stopPropagation) { event.stopPropagation(); } else if (window.event) { window.event.cancelBubble = true; } } }); $(\'.fixed-plugin .background-color span\').click(function() { $(this).siblings().removeClass(\'active\'); $(this).addClass(\'active\'); var new_color = $(this).data(\'color\'); if ($sidebar.length != 0) { $sidebar.attr(\'data\', new_color); } if ($main_panel.length != 0) { $main_panel.attr(\'data\', new_color); } if ($full_page.length != 0) { $full_page.attr(\'filter-color\', new_color); } if ($sidebar_responsive.length != 0) { $sidebar_responsive.attr(\'data\', new_color); } }); $(\'.switch-sidebar-mini input\').on("switchChange.bootstrapSwitch", function() { var $btn = $(this); if (sidebar_mini_active == true) { $(\'body\').removeClass(\'sidebar-mini\'); sidebar_mini_active = false; blackDashboard.showSidebarMessage(\'Sidebar mini deactivated...\'); } else { $(\'body\').addClass(\'sidebar-mini\'); sidebar_mini_active = true; blackDashboard.showSidebarMessage(\'Sidebar mini activated...\'); } // we simulate the window Resize so the charts will get updated in realtime. var simulateWindowResize = setInterval(function() { window.dispatchEvent(new Event(\'resize\')); }, 180); // we stop the simulation of Window Resize after the animations are completed setTimeout(function() { clearInterval(simulateWindowResize); }, 1000); }); $(\'.switch-change-color input\').on("switchChange.bootstrapSwitch", function() { var $btn = $(this); if (white_color == true) { $(\'body\').addClass(\'change-background\'); setTimeout(function() { $(\'body\').removeClass(\'change-background\'); $(\'body\').removeClass(\'white-content\'); }, 900); white_color = false; } else { $(\'body\').addClass(\'change-background\'); setTimeout(function() { $(\'body\').removeClass(\'change-background\'); $(\'body\').addClass(\'white-content\'); }, 900); white_color = true; } }); $(\'.light-badge\').click(function() { $(\'body\').addClass(\'white-content\'); }); $(\'.dark-badge\').click(function() { $(\'body\').removeClass(\'white-content\'); }); }); }); &lt;/script> &lt;script> $(document).ready(function() { demo.checkFullPageBackgroundImage(); }); &lt;/script> &lt;/body> &lt;/html>'

SIDEBAR_ITEM_FILE_TXT = '&lt;a href={LINK}&gt;&lt;i class={ICON}&gt;&lt;/i&gt;&lt;p&gt;{TITLE}&lt;/p&gt;&lt;/a&gt;'

FILE_TO_TXT_MAPPINGS = { MAIN_SITE_FILENAME: MAIN_SITE_FILE_TXT, SIDEBAR_ITEM_FILENAME: SIDEBAR_ITEM_FILE_TXT }

cloudwatch = boto3.client('cloudwatch')

    
def inject(template: str, injections: dict):
    final = template
    for key, value in injections.items():
        final = final.replace(key, value)
    return final


def get_metric_name(metric: tuple) -> str:
    return METRIC_NAME_FORMAT.format(metric[0], metric[1])


def send_metrics(time: float, metric: tuple) -> None:
    print('Sending metrics')
    '''
    def wrapper(*args, **kwargs):
        function(*args, **kwargs)
        metric = kwargs['metric']
    
    '''
    print('made it into the wrapper')
    
    app_name = 'GuyandJaella'
    stage = None
    if 'PROD' in os.environ:
        stage = 'PROD'
    else:
        stage = 'DEV'
    
    unit = metric[2]
    cloudwatch.put_metric_data(Namespace=app_name,
        MetricData = [
                {
                    'MetricName': get_metric_name(metric),
                    'Dimensions': [
                        {
                            'Name': 'By App Version',
                            'Value': os.environ['APP_VERSION']
                        },
                        {
                            'Name': 'By Operation',
                            'Value': metric[1]
                        },
                        {
                            'Name': 'By Stage',
                            'Value': stage
                        },
                    ],
                    'Unit': unit,
                    'Value': time * UNIT_TO_TIME_MULTIPLIER_MAP[unit]
                },
            ])
        


def https_get(file: str, metric: tuple) -> str:
    url = '{}{}'.format(STATIC_URL_PREFIX, file)
    data = urllib.request.urlopen(url)
    data = data.read().decode()
    return data
    
async def fetch_file_txt(file: str, metric: tuple, from_disk=False, from_mem=False) -> str:
    start = time.time()
    if from_mem:
        data = FILE_TO_TXT_MAPPINGS[file]
    elif from_disk:
        with open(file, 'r') as txt:
            data = txt.read()
    else:
        data = https_get(file=file, metric=metric)
    end = time.time()
    send_metrics(end - start, metric)
    return data
    
    
