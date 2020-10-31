import socket

import sys
sys.path.insert(0, './msg')
from packet_pb2 import Environment, Packet
from command_pb2 import Commands, Command

max_vel = 30
def crop(v):
    if v > max_vel:
        v = max_vel
    elif v < -max_vel:
        v = -max_vel
    return v

class Client:
    def __init__(self):
        self.UDP_IP = "192.168.1.11"
        self.UDP_RECEIVE_PORT = 10002
        self.UDP_SEND_PORT = 20011

        self.sock_receive = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP
        
        #addsa
        self.sock_receive.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.sock_receive.bind((self.UDP_IP, self.UDP_RECEIVE_PORT))
        self.sock_receive.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)
        self.sock_receive.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
            socket.inet_aton(self.UDP_RECEIVE_PORT) + socket.inet_aton(self.UDP_IP))

        
        
        #self.sock_receive.bind((self.UDP_IP, self.UDP_RECEIVE_PORT))

        self.sock_send = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

        self.env = Environment()
        
    def receive(self):
        data, addr = self.sock_receive.recvfrom(2048)
        self.env.ParseFromString(data)
        frame = self.env.frame
        return frame.robots_blue, frame.robots_yellow, frame.ball
    
    def send(self, vels, is_yellowteam):
        packet = Packet()
        for i, v in enumerate(vels):
            cmd = Command()
            cmd.id = i
            cmd.yellowteam = is_yellowteam
            cmd.wheel_left = v[0]
            cmd.wheel_right = v[1]
            packet.cmd.robot_commands.append(cmd)
        packet_bytes = packet.SerializeToString()
        self.sock_send.sendto(packet_bytes, (self.UDP_IP, self.UDP_SEND_PORT))
