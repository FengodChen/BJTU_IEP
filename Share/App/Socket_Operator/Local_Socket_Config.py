transfer_endcode = "<$@$#$>fengodchen_EOF<$#$@$>"

server_addrName = "fengodchen_server_app"
vehicleIdentification_addrName = "fengodchen_vehicle_identification_app"
monitor_addrName = "fengodchen_vitual_monitor_app"
laneLine_addrName = "fengodchen_lane_line_recognition_app"

server_yolo_addr1 = (server_addrName, 9190)
server_yolo_addr2 = (vehicleIdentification_addrName, 9190)

yolo_monitor_addr1 = (vehicleIdentification_addrName, 9191)
yolo_monitor_addr2 = (monitor_addrName, 9191)

server_monitor_addr1 = (server_addrName, 9193)
server_monitor_addr2 = (monitor_addrName, 9193)

server_monitor_addr3 = (server_addrName, 9194)
server_monitor_addr4 = (monitor_addrName, 9194)

server_laneline_addr1 = (server_addrName, 9195)
server_laneline_addr2 = (laneLine_addrName, 9195)

laneline_yolo_addr1 = (laneLine_addrName, 9196)
laneline_yolo_addr2 = (vehicleIdentification_addrName, 9196)