from views import homepage, CPU_Usage, Memory_Utilization, Disk_Space, Active_Processes,cpu_usage_data,active_processes_data,disk_space_data,memory_utilization_data


def configure_routes(app):
    app.add_url_rule('/', 'homepage', homepage)
    app.add_url_rule('/CPU_Usage', 'CPU_Usage', CPU_Usage)
    app.add_url_rule('/Memory_Utilization', 'Memory_Utilization', Memory_Utilization)
    app.add_url_rule('/Disk_Space', 'Disk_Space', Disk_Space)
    app.add_url_rule('/Active_Processes', 'Active_Processes', Active_Processes)
    app.add_url_rule('/cpu_usage_data', 'cpu_usage_data', cpu_usage_data)
    app.add_url_rule('/memory_data', 'memory_data', memory_utilization_data)
    app.add_url_rule('/disk_data', 'disk_data', disk_space_data)
    app.add_url_rule('/active_processes_data', 'active_processes_data', active_processes_data)
    