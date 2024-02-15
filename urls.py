from views import homepage, cpu_usage, cpu_usage_data, memory_utilization, memory_utilization_data, disk_space, disk_space_data, active_processes, active_processes_data,ssh_connect,set_localhost

def configure_routes(app):
    app.add_url_rule('/', 'homepage', homepage)
    app.add_url_rule('/cpu_usage', 'cpu_usage', cpu_usage)
    app.add_url_rule('/cpu_usage_data', 'cpu_usage_data', cpu_usage_data)
    app.add_url_rule('/memory_utilization', 'memory_utilization', memory_utilization)
    app.add_url_rule('/memory_data', 'memory_data', memory_utilization_data)
    app.add_url_rule('/disk_space', 'disk_space', disk_space)
    app.add_url_rule('/disk_data', 'disk_data', disk_space_data)
    app.add_url_rule('/active_processes', 'active_processes', active_processes)
    app.add_url_rule('/active_processes_data', 'active_processes_data', active_processes_data)
    app.add_url_rule('/ssh-connect', 'ssh-connect', ssh_connect, methods=[ "POST"])
    app.add_url_rule('/set_localhost', 'set_localhost', set_localhost, methods=["POST"])
