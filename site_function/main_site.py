import os
import asyncio
if 'PROD' in os.environ:
    from site_utils import STATIC_URL_PREFIX, fetch_file_txt, inject, MAIN_SITE_METRIC
    from sidebar import Sidebar
else:
    from .site_utils import STATIC_URL_PREFIX, fetch_file_txt, inject, MAIN_SITE_METRIC
    from .sidebar import Sidebar
#MAIN_SITE_TEMPLATE = '<!DOCTYPE html><html lang="en"><head> <meta charset="utf-8"/> <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no"> <link rel="apple-touch-icon" sizes="76x76" href="assets/img/apple-icon.png"> <link rel="icon" type="image/png" href="assets/img/favicon.png"> <title>Black Dashboard PRO by Creative Tim </title> <link href="https://fonts.googleapis.com/css?family=Poppins:200,300,400,600,700,800" rel="stylesheet"/> <link href="https://use.fontawesome.com/releases/v5.0.6/css/all.css" rel="stylesheet"> <link href="assets/css/nucleo-icons.css" rel="stylesheet"/> <link href="assets/css/black-dashboard.css?v=1.0.0" rel="stylesheet"/> <link href="assets/demo/demo.css" rel="stylesheet"/></head><body class="sidebar-mini"> <div class="wrapper"> <div class="navbar-minimize-fixed"> <button class="minimize-sidebar btn btn-link btn-just-icon"> <i class="tim-icons icon-align-center visible-on-sidebar-regular text-muted"></i> <i class="tim-icons icon-bullet-list-67 visible-on-sidebar-mini text-muted"></i> </button> </div><div class="sidebar"><!-- Tip 1: You can change the color of the sidebar using: data-color="blue | green | orange | red" --> <div class="sidebar-wrapper"> <div class="logo"> <a href="javascript:void(0)" class="simple-text logo-mini"> CT </a> <a href="javascript:void(0)" class="simple-text logo-normal"> Creative Tim </a> </div><ul class="nav">{SIDEBAR_ITEMS}</ul> </div></div><div class="main-panel"> <nav class="navbar navbar-expand-lg navbar-absolute navbar-transparent"> <div class="container-fluid"> <div class="navbar-wrapper"> <div class="navbar-minimize d-inline"> <button class="minimize-sidebar btn btn-link btn-just-icon" rel="tooltip" data-original-title="Sidebar toggle" data-placement="right"> <i class="tim-icons icon-align-center visible-on-sidebar-regular"></i> <i class="tim-icons icon-bullet-list-67 visible-on-sidebar-mini"></i> </button> </div><div class="navbar-toggle d-inline"> <button type="button" class="navbar-toggler"> <span class="navbar-toggler-bar bar1"></span> <span class="navbar-toggler-bar bar2"></span> <span class="navbar-toggler-bar bar3"></span> </button> </div><a class="navbar-brand" href="javascript:void(0)">User Profile</a> </div><button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navigation" aria-expanded="false" aria-label="Toggle navigation"> <span class="navbar-toggler-bar navbar-kebab"></span> <span class="navbar-toggler-bar navbar-kebab"></span> <span class="navbar-toggler-bar navbar-kebab"></span> </button> </div></nav> <div class="col-md-5" style="margin: auto;top: 20%"> </style>> <div class="card card-user"> <div class="card-body"> <p class="card-text"> <div class="author"> <div class="block block-one"></div><div class="block block-two"></div><div class="block block-three"></div><div class="block block-four"></div><a href="javascript:void(0)"> <img class="avatar" src="{GUY_AND_JAELLA_HOME_PIC}" alt="..." style="height: 500px; width:450px"> <h5 class="title">The cutest couple ever</h5> </a> <p class="description"> Guy And Jaella </p></div></p><div class="card-description" style="margin: auto; width: fit-content"> We found perfect love. We\'re meant for each other </div></div><div class="card-footer"> <div class="button-container"> <button href="javascript:void(0)" class="btn btn-icon btn-round btn-facebook"> <i class="fab fa-facebook"></i> </button> <button href="javascript:void(0)" class="btn btn-icon btn-round btn-twitter"> <i class="fab fa-twitter"></i> </button> <button href="javascript:void(0)" class="btn btn-icon btn-round btn-google"> <i class="fab fa-google-plus"></i> </button> </div></div></div></div></div></div><footer class="footer"> <div class="container-fluid"> <ul class="nav"> <li class="nav-item"> <a href="javascript:void(0)" class="nav-link"> Creative Tim </a> </li><li class="nav-item"> <a href="javascript:void(0)" class="nav-link"> About Us </a> </li><li class="nav-item"> <a href="javascript:void(0)" class="nav-link"> Blog </a> </li></ul> </div></footer> </div></div></div><script src="assets/js/core/jquery.min.js"></script> <script src="assets/js/core/popper.min.js"></script> <script src="assets/js/core/bootstrap.min.js"></script> <script src="assets/js/plugins/perfect-scrollbar.jquery.min.js"></script> <script src="assets/js/plugins/moment.min.js"></script> <script src="assets/js/plugins/bootstrap-switch.js"></script> <script src="assets/js/plugins/sweetalert2.min.js"></script> <script src="assets/js/plugins/jquery.tablesorter.js"></script> <script src="assets/js/plugins/jquery.validate.min.js"></script> <script src="assets/js/plugins/jquery.bootstrap-wizard.js"></script> <script src="assets/js/plugins/bootstrap-selectpicker.js"></script> <script src="assets/js/plugins/bootstrap-datetimepicker.js"></script> <script src="assets/js/plugins/jquery.dataTables.min.js"></script> <script src="assets/js/plugins/bootstrap-tagsinput.js"></script> <script src="assets/js/plugins/jasny-bootstrap.min.js"></script> <script src="assets/js/plugins/fullcalendar.min.js"></script> <script src="assets/js/plugins/jquery-jvectormap.js"></script> <script src="assets/js/plugins/nouislider.min.js"></script> <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_KEY_HERE"></script> <script src="assets/js/plugins/chartjs.min.js"></script> <script src="assets/js/plugins/bootstrap-notify.js"></script> <script src="assets/js/black-dashboard.min.js?v=1.0.0"></script> <script src="assets/demo/demo.js"></script> <script>$(document).ready(function(){$().ready(function(){$sidebar=$(\'.sidebar\'); $navbar=$(\'.navbar\'); $main_panel=$(\'.main-panel\'); $full_page=$(\'.full-page\'); $sidebar_responsive=$(\'body > .navbar-collapse\'); sidebar_mini_active=true; white_color=false; window_width=$(window).width(); fixed_plugin_open=$(\'.sidebar .sidebar-wrapper .nav li.active a p\').html(); $(\'.fixed-plugin a\').click(function(event){if ($(this).hasClass(\'switch-trigger\')){if (event.stopPropagation){event.stopPropagation();}else if (window.event){window.event.cancelBubble=true;}}}); $(\'.fixed-plugin .background-color span\').click(function(){$(this).siblings().removeClass(\'active\'); $(this).addClass(\'active\'); var new_color=$(this).data(\'color\'); if ($sidebar.length !=0){$sidebar.attr(\'data\', new_color);}if ($main_panel.length !=0){$main_panel.attr(\'data\', new_color);}if ($full_page.length !=0){$full_page.attr(\'filter-color\', new_color);}if ($sidebar_responsive.length !=0){$sidebar_responsive.attr(\'data\', new_color);}}); $(\'.switch-sidebar-mini input\').on("switchChange.bootstrapSwitch", function(){var $btn=$(this); if (sidebar_mini_active==true){$(\'body\').removeClass(\'sidebar-mini\'); sidebar_mini_active=false; blackDashboard.showSidebarMessage(\'Sidebar mini deactivated...\');}else{$(\'body\').addClass(\'sidebar-mini\'); sidebar_mini_active=true; blackDashboard.showSidebarMessage(\'Sidebar mini activated...\');}// we simulate the window Resize so the charts will get updated in realtime. var simulateWindowResize=setInterval(function(){window.dispatchEvent(new Event(\'resize\'));}, 180); // we stop the simulation of Window Resize after the animations are completed setTimeout(function(){clearInterval(simulateWindowResize);}, 1000);}); $(\'.switch-change-color input\').on("switchChange.bootstrapSwitch", function(){var $btn=$(this); if (white_color==true){$(\'body\').addClass(\'change-background\'); setTimeout(function(){$(\'body\').removeClass(\'change-background\'); $(\'body\').removeClass(\'white-content\');}, 900); white_color=false;}else{$(\'body\').addClass(\'change-background\'); setTimeout(function(){$(\'body\').removeClass(\'change-background\'); $(\'body\').addClass(\'white-content\');}, 900); white_color=true;}}); $(\'.light-badge\').click(function(){$(\'body\').addClass(\'white-content\');}); $(\'.dark-badge\').click(function(){$(\'body\').removeClass(\'white-content\');});});}); </script> <script>$(document).ready(function(){demo.checkFullPageBackgroundImage();}); </script></body></html>'
ASSET_REPLACEMENTS = {'assets/': '{}assets/'.format(STATIC_URL_PREFIX),
                      '{UPLOAD_PLACEHOLER}': '{}Images/image_upload.jpg'.format(STATIC_URL_PREFIX),
                      '{GUY_AND_JAELLA_HOME_PIC}': '{}Images/GuyAndJaella.jpg'.format(STATIC_URL_PREFIX),
                      '{API_DOMAIN}': 'api.petdatatracker.com'}

HTML_PATH_MAPPINGS = {
  '/Test': 'test.html',
  '/': 'home.html',
  '/Dashboard': 'dashboard.html',
  '/Snake/New': 'newSnake.html',
  '/Snakes': 'snakes.html'}

class MainSite():
  def __init__(self):
    pass

  async def create_html(resource: str) -> str:
    template_uri = HTML_PATH_MAPPINGS[resource]
    main_template_task = asyncio.create_task(fetch_file_txt(file=template_uri, metric=MAIN_SITE_METRIC, from_disk=True))
    sidebar_task = asyncio.create_task(Sidebar(template_uri=os.environ['SIDEBAR_URI']).get())
    main_injections = ASSET_REPLACEMENTS
    main_template = await main_template_task
    main_html = inject(main_template, main_injections)
    sidebar_html = await sidebar_task

    html = main_html.replace('{SIDEBAR_ITEMS}', sidebar_html)

    return html