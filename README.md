# Information-extraction-of-devices-behind-NAT-using-WebRTC


IP addresses are the core part of the modern Internet, and they are necessary to communicate with other
devices on the network. The Internet is expanding at a tremendous rate, and along with it, security flaws
are also growing. Malicious users on the Internet constantly exploit these security flaws and take
advantage of them, and in most cases, they cannot be identified. Identifying users on the Internet is a
complex task mainly due to the number of layers in the network and technologies like VPNs, which
specifically provide services to hide a user's identity. The first layer is the NAT, and there is no direct
method to identify the user behind the NAT. This article will discuss a solution to find information about
the user, including the private IP behind a NAT device from a browser session. The solution exploits
WebRTC, which is a popular technology used in peer-peer communication without any intermediary
server. The method is demonstrated on a virtual network in Mininet with multiple hosts trying to
communicate with a server through a NAT. The feasibility of the solution is shown by comparing results
across popular browsers, and a network map is formed displaying all the private IP addresses hidden
behind the Public IP of NAT.
