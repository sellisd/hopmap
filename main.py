import click
import subprocess
from scapy.all import *
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import requests


def draw_map_with_arrows(locations):
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    for i in range(len(locations)-1):
        lons = [locations[i][1], locations[i+1][1]]
        lats = [locations[i][0], locations[i+1][0]]
        ax.plot(lons, lats, 'o-', transform=ccrs.Geodetic(), color='red')
        ax.arrow(lons[0], lats[0], lons[1]-lons[0], lats[1]-lats[0], color='blue', transform=ccrs.Geodetic(), width=0.5)
    plt.show()

def geolocate(ip):
  response = requests.get(f'http://ip-api.com/json/{ip}')
  data = response.json()
  return data


@click.command()
@click.argument('host')
def traceroute(host):
  command = ['traceroute', '-n',  host]
  process = subprocess.Popen(command, stdout=subprocess.PIPE)
  first_line = True
  locations = []
  while True:
    line = process.stdout.readline().decode('utf-8')
    if not line:
      break
    if first_line:
      first_line = False
      continue
    data = parse_traceroute_line(line)
    print(data)
    locations.append([data[1], data[2]])
  draw_map_with_arrows(locations)

def parse_traceroute_line(line):
  parts = line.split()
  hop_num = parts[0]
  hop_name = parts[1] if len(parts) > 1 else None
  hop_ip = parts[2].strip('()') if len(parts) > 2 else None
  longitude = None
  latitude = None
  if hop_name != '*':
    data = geolocate(hop_name)
    if data['status'] == 'success':
      longitude = data['lon']
      latitude = data['lat']
  return (hop_num, longitude, latitude, hop_ip)


if __name__ == '__main__':
    traceroute()
