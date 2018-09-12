import json
from influxdb import InfluxDBClient

1422568543702900257
msg = b'{"node_id":"16700204541000610066a000a00000c1","ts":1536676839497,"phase_1_voltage_rms":0.05,"phase_2_voltage_rms":0.04,"phase_3_voltage_rms":0.01,"phase_1_current_rms":1.27,"phase_2_current_rms":1.27,"phase_3_current_rms":0.04,"n_line_calculated_current_rms":2.56,"phase_1_frequency":49.94,"phase_2_voltage_phase":-7.4,"phase_3_voltage_phase":-12.1,"phase_1_voltage_thd_n":56.23,"phase_2_voltage_thd_n":80.49,"phase_3_voltage_thd_n":0,"phase_1_current_thd_n":11.84,"phase_2_current_thd_n":12.58,"phase_3_current_thd_n":22.93,"phase_1_active_power":0,"phase_2_active_power":0,"phase_3_active_power":0,"phase_1_reactive_power":-1,"phase_2_reactive_power":-1,"phase_3_reactive_power":0,"phase_1_apparent_power":0,"phase_2_apparent_power":0,"phase_3_apparent_power":0,"phase_1_power_factor":1,"phase_2_power_factor":0.83,"phase_3_power_factor":0,"phase_1_active_fundamental":0,"phase_2_active_fundamental":0,"phase_3_active_fundamental":0,"phase_1_active_harmonic":0,"phase_2_active_harmonic":0,"phase_3_active_harmonic":0,"phase_1_forward_active":0,"phase_2_forward_active":0,"phase_3_forward_active":0,"phase_1_reverse_active":0,"phase_2_reverse_active":0,"phase_3_reverse_active":0,"phase_1_forward_reactive":0,"phase_2_forward_reactive":0,"phase_3_forward_reactive":0,"phase_1_reverse_reactive":0,"phase_2_reverse_reactive":0,"phase_3_reverse_reactive":0,"phase_1_apparent_energy":0,"phase_2_apparent_energy":0,"phase_3_apparent_energy":0,"measured_temperature":36,"input_1_status":0,"input_2_status":0,"input_3_status":0}'

data = json.loads(msg)
node_id = data["node_id"]
ts = data["ts"]
del data["node_id"]
del data["ts"]

for field in data:
    data[field] = float(data[field])

influxdb_msg = [{"measurement": "pmc_data"}]
influxdb_msg[0]["timestamp"] = ts
influxdb_msg[0]["tags"] = {"host": node_id}
influxdb_msg[0]["fields"] = data

influxdb = InfluxDBClient('metrum.ijs.si', 8086, 'pmc', 'PMC.meritve.param', 'pmc')

influxdb.write_points(influxdb_msg)

print(json.dumps(influxdb_msg))