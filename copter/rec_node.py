import rospy
from record.record import Record
from srv.null import NullResponse, NullRequest

class RecServer:
    def __init__(self) -> None:
        self.rec = Record()

    def start_rec(self, req):
        self.rec.start_recording()
        return NullResponse()

    def stop_rec(self, req):
        self.rec.stop_recording()
        return NullResponse()

    def init_server(self):
        rospy.init_node('add_two_ints_server')

        start_srv = rospy.Service('start', self.start_rec, NullRequest)
        stop_srv = rospy.Service('stop', self.start_rec, NullRequest)

        rospy.spin()

if __name__ == "__main__":
    server = RecServer()
    server.init_server()