# How to run OpenVPN on IPv6 networks in a container
## Or: Why interactive hacking lessons are hard and how to make it better

TL;DR: See [The finicky details](#the-finicky-details) for the code to get OpenVPN working
on IPv6 networks in a container.

In college, while trying to develop content and tools for the Cybersecuriy Club,
we became interested in providing low-friction hacking environments for members
of the club to easily get up to speed with Kali Linux and the tools within it.
We were fans of [Hack the Box](XXXXXXXXXXX) for hacking challenges, which uses a
(IPv6) VPN for users to access attackable machines. Advanced hackers in the club
already had Kali installed as a VM and were proficient with Linux and VPNs. Our
newer members, on the other hand, usually lacked Linux skills and frequently
struggled with installing a Kali VM [1]. We could, and often did, ask members of
the club to spend a little bit of their own time acquiring a Kali Linux VM so we
could run club sessions around Kali tools, but this doesn't work:

- Someone attending their first meeting during a Kali section will be bored because they won't be
  able to participate; they had no idea they would need a Kali VM [2]
- Someone without sufficient hardware to run a VM (Chromebooks, low-spec laptops of all flavors)
  will be left out
- College students are busy and lazy. They will either forget to install the VM or not want to
  take the time to do so. If a club wants to grow (and we did at the time), lowering the barrier
  to participation is key.
- New club members are inexperienced with VMs and will inevitably need in-person help from
  more experienced club members to end up with a functioning VM.

So, we wanted a hardware-agnostic, quickly-available environment for club
members to use penetration testing tools (or any other software relevant to a
lesson or session). We considered a few different options, including integrating
with [JupyterHub](https://jupyter.org/hub), but ultimately settled on rolling
our own solution with Docker + K8s because we were most familiar with those
tools and were granted more rapid prototyping as a result [3]. Naturally,
implementation details were the bane of our existence. While containers are
an excellent tool for quickly spinning up fresh, individual environments, they
come with their own challenges in the networking world. By default, most Docker
containers will be unable to connect to an OpenVPN server or do IPv6 networking
of any kind. Getting around this requires some special configuration steps
while building and running the container:

## The finicky details

To open a tunnel (IPv4 or v6), containers need the following:
- The `NET_ADMIN` capability.
- The `/dev/net/tun` file.
  Creatable (if it does not exist) with the following code:
  ```
  mkdir -p /dev/net
  mknod /dev/net/tun c 10 200
  chmod 0666 /dev/net/tun
  ```
  
To have IPv6 capability, containers need the following:
- The `net.ipv6.conf.all.disable_ipv6` sysctl un-disabled (it is disabled by default). 
- (If running under the Docker daemon) The Docker daemon will need IPv6 enabled ([official docs](https://docs.docker.com/config/daemon/ipv6/)).

Links I used to determine this information:
* [Docker and IPv6](https://docs.docker.com/v17.09/engine/userguide/networking/default_network/ipv6/#how-ipv6-works-on-docker)
* [OpenVPN and IPv6 in containers](https://github.com/dperson/openvpn-client/issues/75)
* [/dev/net/tun explanation Reddit post #1](https://www.reddit.com/r/docker/comments/bog7gy/help_with_error_cannot_open_tuntap_dev_devnettun/)
* [/dev/net/tun explanation Reddit post #2](https://www.reddit.com/r/docker/comments/4cw758/accessing_tuntap_device_inside_of_a_docker/)
* [/dev/net/tun creation issue](https://github.com/haugene/docker-transmission-openvpn/issues/538)
* [/dev/net/tun creation code](https://github.com/haugene/docker-transmission-openvpn/blob/dev/openvpn/start.sh#L8)

## Bonus: 

## Notes

[1] The two main ways of getting a Kali VM are by installing it via the official ISOs or pre-built VM
images. At the time when I was working on this, the pre-built VM images were available from Offensive
Security, but now seem to be available directly from the Kali website. Both methods of getting a VM
required a hypervisor of some sort, necessitating a small download and install time. Installing via
an ISO tends to be quick on modern hardware but will still take up a _substantial_ portion of club time,
especially if issues are encountered. Pre-built VM images are ideal, but in my ~4 years of experience
in the club at least one person always ran into some bizarre problem importing the VM image in their
hypervisor of choice causing a delay or forcing them to be left out.

[2] I'm a stront believer that interactivity is a key part of learning and also contributes to enthusiasm
about subjects and therefore repeat attendance of the club.

[3] Rapid prototyping was doubly-important because the club member I was working on this with and I were
double-dipping by using this project as a final for a course we shared.
