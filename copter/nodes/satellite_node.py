import rospy as ros
import std_srvs.srv as srv
import std_msgs.msg as msg

class SatelliteNode:
    def __init__(self) -> None:
        ros.init_node("satellite_node")

        if not ros.has_param("scheduler_topic_name"):
            ros.logerr("Run Schedulurer node first")
            exit(1)

        self.scheduler_topic_name = ros.get_param("scheduler_topic_name")
        
        self.start_srv = ros.Service("start", srv.Empty, self.start) # declare service type
        self.stop_pub = ros.Publisher(f"{self.scheduler_topic_name}_stop", msg.String)

    def start(req: srv.EmptyRequest):
        return srv.EmptyResponse()

    def stop(self):
        self.stop_pub.publish("node end working")

if __name__ == "__main__":
    node = SatelliteNode() 
    ros.spin()
