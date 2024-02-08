from views import homepage, CPU_Usage, Memory_Utilization, Disk_Space, Active_Processes, collect_system_info


def configure_routes(app):
    app.add_url_rule('/', 'homepage', homepage)
    app.add_url_rule('/CPU_Usage', 'CPU_Usage', CPU_Usage)
    app.add_url_rule('/Memory_Utilization', 'Memory_Utilization', Memory_Utilization)
    app.add_url_rule('/Disk_Space', 'Disk_Space', Disk_Space)
    app.add_url_rule('/Active_Processes', 'Active_Processes', Active_Processes)
    app.add_url_rule('/collect_system_info', 'collect_system_info', collect_system_info)