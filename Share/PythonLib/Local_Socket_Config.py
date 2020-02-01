transfer_endcode = "<$@$#$>fengodchen_EOF<$#$@$>"

server_addrName = "fengodchen_server_app"
vehicleIdentification_addrName = "fengodchen_vehicle_identification_app"
monitor_addrName = "fengodchen_vitual_monitor_app"
laneLine_addrName = "fengodchen_lane_line_recognition_app"

server_yolo_addr1 = (server_addrName, 1080)
server_yolo_addr2 = (vehicleIdentification_addrName, 1080)

yolo_monitor_addr1 = (vehicleIdentification_addrName, 1081)
yolo_monitor_addr2 = (monitor_addrName, 1081)

server_monitor_addr1 = (server_addrName, 1083)
server_monitor_addr2 = (monitor_addrName, 1083)

server_monitor_addr3 = (server_addrName, 1084)
server_monitor_addr4 = (monitor_addrName, 1084)

server_laneline_addr1 = (server_addrName, 1085)
server_laneline_addr2 = (laneLine_addrName, 1085)

laneline_yolo_addr1 = (laneLine_addrName, 1086)
laneline_yolo_addr2 = (vehicleIdentification_addrName, 1086)

laneline_yolo_addr3 = (laneLine_addrName, 1087)
laneline_yolo_addr4 = (vehicleIdentification_addrName, 1087)